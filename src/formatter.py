
def wpa2_akm(id):

    opts = { 
        0: 'reserved',
        1: 'eap',
        2: 'psk',
        3: 'ft/eap',
        4: 'ft/psk',
        5: 'eap/sha256',
        6: 'psk/sha256',
        7: 'tdls',
        8: 'sae',
        9: 'ft/sae',
    }

    return [opts.get(k, 'unknown') for k in id['IE_KEY_RSN_AUTHSELS']]

def wpa_akm(id):

    opts = {
        0: 'reserved',
        1: 'eap',
        3: 'psk'
    }

    return [opts.get(k, 'unknown') for k in id['IE_KEY_WPA_AUTHSELS']]

def wpa2_ciphers(id):

    opts = {
        0: '@group',
        1: 'wep-40',
        2: 'tkip', #RC4
        3: 'reserved',
        4: 'ccmp', #AES
        5: 'wep-104',
        6: 'bip',
        7: '@group-not-allowed'
    }

    return opts.get(id, 'unknown')

def wpa_ciphers(id):

    opts = {
        0: '@group',
        1: 'wep-40',
        2: 'tkip', #RC4
        3: 'reserved',
        4: 'reserved', #AES
        5: 'wep-104'
    }

    return opts.get(id, 'unknown')

def decode_encryption(n):

    ret = []
    if 'RSN_IE' in n:
        ret.append({
            'type' : 'wpa2',
            'auth' : wpa2_akm(n['RSN_IE']),
            'unicast': [wpa2_ciphers(c) for c in n['RSN_IE']['IE_KEY_RSN_UCIPHERS']],
            'group' : wpa2_ciphers(n['RSN_IE']['IE_KEY_RSN_MCIPHER'])
        })
        
    if 'WPA_IE' in n:
        ret.append({
            'type' : 'wpa',
            'auth' : wpa_akm(n['WPA_IE']),
            'unicast': [wpa_ciphers(c) for c in n['WPA_IE']['IE_KEY_WPA_UCIPHERS']],
            'group' : wpa_ciphers(n['WPA_IE']['IE_KEY_WPA_MCIPHER'])
        })

    return ret

def country(n):
    if '80211D_IE' in n and 'IE_KEY_80211D_COUNTRY_CODE' in n['80211D_IE']:
        return n['80211D_IE']['IE_KEY_80211D_COUNTRY_CODE']
    else:

        return '--'

def process_network(n):
    ret = dict()
    ret['bssid'] = n['BSSID']
    ret['ssid'] = n['SSID_STR'] #{ 'raw': n['SSID'], 'encoded': n['SSID_STR'] }
    ret['security'] = decode_encryption(n)
    ret['radio'] = {   
        'rssi' : n['RSSI'],
        'noise' : n['NOISE'],
        'channel': {
            'current': n['CHANNEL'],
            'flags' : n['CHANNEL_FLAGS']
        },
        'country' : country(n),
        'mode' : n['AP_MODE'],
    }
    ret['HT'] = 'HT_IE' in n # Just mimic Apple printout for now

    return ret

def parser(p):

    return list(map(lambda x: process_network(x), p))
