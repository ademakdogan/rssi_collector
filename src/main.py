import argparse
from collector import get_all_values, collect_rssi

if __name__ == "__main__":
    
    ap = argparse.ArgumentParser()
    ap.add_argument("-l", "--label", required= True)
    ap.add_argument("-s", "--save_path", required= True)
    ap.add_argument("-t", "--time_limit", required= False, default= 60)
    args = vars(ap.parse_args())

    raw_result_list = get_all_values(int(args["time_limit"]))
    collect_rssi(raw_result_list, args["label"],args["save_path"])
