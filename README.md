# RSSI collector

In this project, the BSSID and received signal strength indicator (RSSI) of nearby wireless devices are recorded (For Macos)
For installation (only need pandas) :  

```
make install
``` 
Usage:  

```
python src/main.py -l 0 -s /Users/.../.../sample.csv -t 5
```
* __-l__ : You can use this project for deep learning. If you want to label your data you can use this parameter.
* __-s__ : The path where the obtained data will be stored as csv file (absolute path)
* __-t__ : How many seconds work (default = 60)

_In [config.json](config.json), you can change airport path for your mac_   

In addition, recording is completed when you press ctrl + c during process. You don't need to wait for the time to expire.  

Result:
```
Starting..
0
1
2
Data is being processed.
Saved.
```

The above 0.1,2 values ​​are not seconds. They are the number of loops. Each cycle takes more than 1 second. 

## TODO

* Linux version