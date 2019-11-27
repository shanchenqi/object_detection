#!/usr/bin/bash


cd ~/obsutil_linux_arm64_5.1.10/
./obsutil config -i=RWRJVJJTGBRUTWEXGNV3 -k=TZ8f6eEVLrtpgVYcdKwyXXxgpQFxj7cmfk6ZzQmb -e=https://obs.cn-north-1.myhuaweicloud.com

./obsutil ls obs://cafe-ssd/ -s -d

read -p "Please input new_version: " str

path1=obs://cafe-ssd/
versions=str
class=/classes.txt
model=/object_detection.om
version=${path1}${str}${class}
echo $version 
./obsutil cp ${path1}${str}${class}  ~/sample-objectdetection-python/objectdetectionapp/
./obsutil cp ${path1}${str}${model}  ~/sample-objectdetection-python/MyModel/


read -p "Do you want to start now:(y/n) " startnow

if [ ${startnow} = y ] ;then
  bash ~/sample-objectdetection-python/objectdetectionapp/script/killme.sh python
  cd ~/sample-objectdetection-python/objectdetectionapp
  bash ~/sample-objectdetection-python/script/run_agent.sh
fi

