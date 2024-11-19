# grafana 数据可视化平台
- 是一款开源的数据可视化平台
- 常常与其他数据采集软件（如prometheus）使用

----------------------------------------------------------------------------

## 安装
- 官网
```shell
https://grafana.com/
```
- 下载
```shell
wget https://dl.grafana.com/oss/release/grafana-11.3.0.linux-amd64.tar.gz
```
- 解压
```shell
tar -xzvf grafana-11.3.0.linux-amd64.tar.gz
```
- 进入路径
```shell
cd grafana-v11.3.0
```
- 创建目录
```shell
mkdir logs
mkdir data
mkdir plugins
```
- 获取当前路径的完整路径，后面配置文件要用
```shell
pwd
```
- 比如我得到的路径是
```shell
/root/promethus/grafana-v11.3.0
```
- 进入目录
```shell
cd bin
```
- 创建环境变量配置文件
```shell
vi grafana.cnf
```
- 注意，下文中的 GRAFANA_HOME 请替换为上文得到的完整路径
```shell
#定义用户，我最开始使用grafana，不知道哪个文件授权有问题导致服务没法启动
GRAFANA_USER=root
#定义组 
GRAFANA_GROUP=root
#grafana的工作目录，tar包解压的路径
# GRAFANA_HOME=$GRAFANA_HOME
#grafana的日志文件，最好自己手动建好
LOG_DIR=$GRAFANA_HOME/logs
#grafana的数据存储路径，最好自己手动建好
DATA_DIR=$GRAFANA_HOME/data
#打开的最大文件数
MAX_OPEN_FILES=10000
#grafana的主配置文件夹
CONF_DIR=$GRAFANA_HOME/conf
#grafana的主配置文件
CONF_FILE=$GRAFANA_HOME/conf/sample.ini
RESTART_ON_UPGRADE=true
#grafana的组件目录，自己手动建好
PLUGINS_DIR=$GRAFANA_HOME/plugins
#grafana的provisioning的路径，tar包解压出来就有
PROVISIONING_CFG_DIR=$GRAFANA_HOME/conf/provisioning
# Only used on systemd systems
#pid存放路径，自己手动建好
PID_FILE_DIR=$GRAFANA_HOME/bin/pid.grafana
```
- 编写启动脚本
```shell
vi start.sh
```
```shell
# default web port 9090
WEB_PORT=9200

CONFIG_FILE=./grafana.cnf

PID_FILE=pid.grafana
LOG_FILE=log.grafana

echo grafana starting ...

cd ../
export GRAFANA_HOME=`pwd`
export GF_SERVER_HTTP_PORT=$WEB_PORT
cd bin
nohup ./grafana-server --config=$CONFIG_FILE > $LOG_FILE 2>&1 & echo $! > $PID_FILE

echo grafana started on web : http://localhost:$WEB_PORT/
```
- 编写停止脚本
```shell
vi stop.sh
```
```shell
_p_pid=

PID_FILE=pid.grafana
PROCESS_NAME=grafana-server

if [[ -n "${PID_FILE}" ]]; then
  _p_pid=$(cat ${PID_FILE})
  echo -e "\033[0;34m pid file \033[0m  find pid= \033[0;34m $_p_pid \033[0m "
fi

if [[ -n "${_p_pid}" ]]; then
  _p_pc=`ps -ef | grep -v grep | awk '{print $2}' | grep $_p_pid | wc -l`
  if [ "$_p_pc" == "0" ]; then
    _p_pid=
  fi
fi

if [ "${_p_pid}" == "" ]; then
  _p_pid=`ps -ef | grep -v grep | grep $PROCESS_NAME | awk '{print $2}'`
  echo -e "\033[0;34m process name \033[0m  find pid= \033[0;34m $_p_pid \033[0m "
fi

if [ "${_p_pid}" == "" ]; then
  echo process has already stoped.
  exit
fi

echo kill process $_p_pid ...
kill -9 $_p_pid

echo killed process $_p_pid .
```
- 添加执行权限
```shell
chmod +x *.sh
```
- 启动服务
```shell
./start.sh
```
- 访问链接
```shell
http://localhost:9200/
```
- 默认第一次登录进去
- 要求更改密码

----------------------------------------------------------------------------

## 配置prometheus数据源
- 点击，菜单-Connections-Data Source
- 点击，Add Data Source
- 选择，Prometheus
- 填写名称，prometheus
- 填写prometheus的服务地址，http://localhost:9090
- 看下其他有没有需要特别配置的
- 没有的话，直接拿到最后
- 点击，Save & Test
- 会弹出一个提醒
- 点击，Explore View
- 现在prometheus数据源就配置完成了


----------------------------------------------------------------------------

## 添加监控面板
- 点击，菜单-Dashboards
- 点击按钮，New
- 点击按钮的下拉选项，Import
- 会显示一个填写页面，找到按钮，Load
- 提示可以输入URL或者ID
- 上方有一个链接，grafana.com/dashboards
- 新页面访问这个链接
- 或者也可以访问这个链接
```shell
https://grafana.com/grafana/dashboards/
```
- 下面以添加node_exporter的面板为例
- 在新打开的页面，搜索node
- 找到面板，Node Exporter Full
- 点击进入
- 此时，浏览器URL路径变成了这个
```shell
https://grafana.com/grafana/dashboards/1860-node-exporter-full/
```
- 直接复制这个URL
- 回到Import的页面，粘贴这个URL到Load按钮的输入框
- 点击按钮，Load
- 此时，会显示几个内容，Name,Folder,Prometheus三个输入框
- 可以根据需要，改个Name名字
- 最后，一定要记得，选择一个Prometheus数据源
- 也就是上面刚配置的数据源
- 点击按钮，Import
- 完成配置面板
- 这样，就可以在菜单[Dashboard]中查看到刚才的名字面板了


----------------------------------------------------------------------------

## 告警配置

