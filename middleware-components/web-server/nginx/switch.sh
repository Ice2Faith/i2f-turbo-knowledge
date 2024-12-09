#!/bin/bash

Option=$1

SERVER=192.168.1.100:8080

# 如果有第二个参数，则第二个参数就是server的值
# 将会覆盖默认的值
if [[ -n "$2" ]]; then
  SERVER=$2
fi

CONFIG_FILE=conf/nginx.conf

function help()
{
    echo -e "\033[0;31m please input 1st arg:Option \033[0m"
    echo -e "    options: \033[0;34m {up|u|down|d} \033[0m"
    echo -e "\033[0;34m up/u    \033[0m : up server $SERVER"
    echo -e "\033[0;34m down/d     \033[0m : down server $SERVER"

    exit 1
}

function up(){
  cp $CONFIG_FILE $CONFIG_FILE.bak
  sed -i "/^[[:space:]]*#[[:space:]]*server[[:space:]]*$SERVER/s/^#//" $CONFIG_FILE
  ./sbin/nginx -s reload
  echo -e "up server \033[0;34m $SERVER    \033[0m"
}

function down(){
  cp $CONFIG_FILE $CONFIG_FILE.bak
  sed -i "/^[[:space:]]*server[[:space:]]*$SERVER/s/^/#/" $CONFIG_FILE
  ./sbin/nginx -s reload
  echo -e "down server \033[0;34m $SERVER    \033[0m"
}

if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: config file not found : $CONFIG_FILE"
    exit 1
fi

case $Option in
  up)
  up;;
  u)
  up;;
  down)
  down;;
  d)
  down;;
  *)
  help;;
esac
