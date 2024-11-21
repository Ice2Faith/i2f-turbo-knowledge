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
- 进入目录
```shell
cd bin
```
- 统一启停脚本
  - 对应变更以下内容
  - 使用
  - 启动： ./processctl.sh start
  - 停止： ./processctl.sh stop
```shell
vi processctl.sh
```
```shell

# 应用名称，用于表示应用名称，仅显示使用
APP_NAME=grafana

# 进程名称，用于ps查找进程的关键字
PROCESS_NAME=grafana-server
# 进程绑定的端口，用于netstat查找进程
BIND_PORT=9200

# 工作路径，脚本开始运行时候，将会先cd进入此路径
WORK_DIR=

# 启动与停止命令
# 安装路径
export GRAFANA_HOME=`realpath ../`
# WEB端口
export GF_SERVER_HTTP_PORT=$BIND_PORT
#定义用户，我最开始使用grafana，不知道哪个文件授权有问题导致服务没法启动
export GRAFANA_USER=root
#定义组 
export GRAFANA_GROUP=root
#grafana的日志文件，最好自己手动建好
export GF_PATHS_LOGS=logs
#grafana的数据存储路径，最好自己手动建好
export GF_PATHS_DATA=data
#grafana的组件目录，自己手动建好
export GF_PATHS_PLUGINS=plugins
#grafana的provisioning的路径，tar包解压出来就有
export GF_PATHS_PROVISIONING=conf/provisioning

CONFIG_FILE=$GRAFANA_HOME/conf/defaults.ini
START_CMD="./grafana-server --config=$CONFIG_FILE --homepath=$GRAFANA_HOME --pidfile=metas/pid.grafana-server"
STOP_CMD=

# 是否使用nohup后台运行启动命令
ENABLE_NOHUP=$BOOL_TRUE

# 是否具有专门的停止命令
ENABLE_STOP_CMD=$BOOL_FALSE

# 在执行启动或者停止命令之前执行的内容
function beforeStart(){
  echo grafana started on web : http://localhost:$BIND_PORT/
  echo "starting ..."
}

function beforeStop(){
  echo "stopping .."
}
```
- 添加执行权限
```shell
chmod +x *.sh
```
- 启动服务
```shell
./processctl.sh restart
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

- 这里介绍email邮件告警的配置
- 需要准备一个已经开通了SMTP的邮箱账号
- 用来充当邮件的发送人
- 下面以网易163邮箱为例
- 打开163官网

```shell
https://mail.163.com/
```

- 登录后，上方找到[设置]-[POP3/SMTP/IMAP]
- 找到[开启服务]-[POP3/SMTP服务]
- 点击开启，继续按照流程完成
- 最后，你会得到一个授权码
- 这个授权码就是后面要用的密码
- 先保存下来，后面使用
- 最下面写明了基本配置

```text
服务器地址：
  POP3服务器: pop.163.com
  SMTP服务器: smtp.163.com
  IMAP服务器: imap.163.com
安全支持：
  POP3/SMTP/IMAP服务全部支持SSL连接
```

- 一会儿就要使用SMTP服务器
- 上面，就完成了开通一个SMTP的邮箱账号
- 下面，开始配置grafana的发件配置
- 进入安装路径

```shell
cd grafana-v11.3.0
```

- 编辑配置文件

```shell
vi conf/defaults.ini
```

- 找到[smtp]节点并修改以下配置
- 注意，此类ini文件用井号或分好座位注释符号

```shell
[smtp]
enabled = true # 开启配置
host = smtp.163.com:25 # 163的SMTP服务器，默认25端口
user = xxx@163.com # 你的邮箱账号
password = "授权码" # 前面获得的邮箱授权码
cert_file =
key_file =
skip_verify = false # 关闭校验
from_address = xxx@163.com # 发件人，一般就用邮箱账号
from_name = Grafana # 发件人名，自己定义就行
ehlo_identity =
startTLS_policy =
enable_tracing = false
```

- 重启

```shell
cd bin
./processctl.sh restart
```

- 到这里，就完成了告警发件邮箱的配置
- 下面，开始配置邮件告警