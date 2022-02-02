
import plistlib
import subprocess
from formatter import parser
import pandas as pd
import os
import json
import time

def config_data():

    base_path = base_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(os.path.dirname(os.path.normpath(base_path)), "config.json")
    with open(config_path, 'r') as fp:
        config = json.load(fp)

    return [config["airport_path"] + " -xs"]

def get_all_values(time_limit):

    args = config_data()
    raw_result_list = []
    counter = 0
    print("Starting..")
    start = time.time()
    while True:
        
        try:
            p = subprocess.Popen(args, stdout=subprocess.PIPE, shell = True)
            stdout = p.communicate()[0]
            aa = stdout.decode("utf-8")
            p = plistlib.loads(aa.encode('utf-8'))
            result = parser(p)
            raw_result_list.append(result)
            print(counter)
            counter += 1
            end = time.time()
            if int(end - start) >= time_limit:

                return raw_result_list

        except KeyboardInterrupt:

            return raw_result_list
        
        except:

            #raise Exception("Unexpected situation here.") 
            print("Try again..")
            time.sleep(1)
            continue

def collect_rssi(raw_result_list, label, save_path):
    
    print("Data is being processed.")
    row_list = []
    for i in range(len(raw_result_list)):
        temp_dict = {}
        for j in range(len(raw_result_list[i])):
            # if raw_result_list[i][j]["bssid"] not in column_names: column_names.append(raw_result_list[i][j]["bssid"])
            temp_dict[raw_result_list[i][j]["bssid"]] = raw_result_list[i][j]["radio"]["rssi"]
            temp_dict["label"] = label 
        row_list.append(temp_dict)
    result = pd.DataFrame(row_list, dtype=int).fillna(0)
    result.to_csv(save_path)
    print("Saved.")
    
    return

    


