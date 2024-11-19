# prometheus 运维监控告警平台
- 是一款开源的运维监控指标采集平台
- 常常与其他可视化软件（如grafana）结合
- 构建可视化的运维监控告警一体化平台
- 其中依托prometheus强大的采集插件(exporter)进行指标数据的采集
- 但是自身提供的可视化能力有限
- 因此，常常与grafana这个可视化软件结合
- grafana提供了强大的数据介入能力与可视化配置能力
- 能够丰富的展示各类数据指标

----------------------------------------------------------------------------

## 安装
- 官网
```shell
https://prometheus.io/
```
- 地址
```shell
https://prometheus.io/download/
```
- 下载
```shell
wget https://github.com/prometheus/prometheus/releases/download/v3.0.0/prometheus-3.0.0.linux-amd64.tar.gz
```
- 解压
```shell
tar -xzvf prometheus-3.0.0.linux-amd64.tar.gz
```
- 重命名
```shell
mv prometheus-3.0.0.linux-amd64 prometheus-3.0.0
```
- 进入路径
```shell
cd prometheus-3.0.0
```
- 查看配置文件
```shell
cat prometheus.yml
```
- 将会以中文描述添加说明到配置文件中
```yml
# my global config
# 全局配置
global:
  # 数据抓取频率，每隔多长时间从scrape_configs配置的exporter节点中抓取指标数据
  scrape_interval: 15s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
  # 规则检查频率，每隔多长时间从rule_files配置的规则中，判断是否要触发规则执行
  evaluation_interval: 15s # Evaluate rules every 15 seconds. The default is every 1 minute.
  # scrape_timeout is set to the global default (10s).

# Alertmanager configuration
# 告警配置
alerting:
  alertmanagers:
    - static_configs:
        - targets:
          # - alertmanager:9093

# Load rules once and periodically evaluate them according to the global 'evaluation_interval'.
# 规则配置
rule_files:
# - "first_rules.yml"
# - "second_rules.yml"

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
# 抓取配置，后面加的各种exporter端点，要接入prometheus,就要配置在这边，让prometheus去抓取数据
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  # 这是一个列表配置，可以配置多个，job_name唯一即可
  # 一般，job_name表示一类相同属性的端点，比如，干同一件事的服务器，同一个服务
  # 默认配置，就会有一个prometheus服务
  - job_name: "prometheus"

    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.
    
    static_configs:
      # 在target中添加具体的端点实例，比如某个service在三台服务器以负载均衡的模式部署
      # 则，这里就可以添加三台主机的地址
      - targets: ["localhost:9090"]
```
```shell
vi start.sh
```
```shell
# default web port 9090
WEB_PORT=9090

CONFIG_FILE=./prometheus.yml

PID_FILE=pid.prometheus
LOG_FILE=log.prometheus

echo prometheus starting ...
nohup ./prometheus --web.enable-lifecycle --web.listen-address=:$WEB_PORT --config.file=$CONFIG_FILE > $LOG_FILE 2>&1 & echo $! > $PID_FILE

echo prometheus started on web : http://localhost:$WEB_PORT/
```
- 编写停止脚本
```shell
vi stop.sh
```
```shell
_p_pid=

PID_FILE=pid.prometheus
PROCESS_NAME=prometheus

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
- 启动
```shell
./start.sh
```
- 浏览器访问
```shell
http://localhost:9090/
```

----------------------------------------------------------------------------

## 插件安装
- 地址
```shell
https://prometheus.io/docs/instrumenting/exporters/
```

----------------------------------------------------------------------------

### 服务器监控(node_exporter)
- 需要部署在被检测的主机上
- 可以观测内存、CPU、网络、磁盘等资源情况
- 地址
```shell
https://prometheus.io/download/#node_exporter
```
- 下载
```shell
wget https://github.com/prometheus/node_exporter/releases/download/v1.8.2/node_exporter-1.8.2.linux-amd64.tar.gz
```
- 解压
```shell
tar -xzvf node_exporter-1.8.2.linux-amd64.tar.gz
```
- 重命名
```shell
mv node_exporter-1.8.2.linux-amd64 node_exporter-1.8.2
```
- 进入路径
```shell
cd node_exporter-1.8.2
```
- 编辑启动脚本
```shell
vi start.sh
```
```shell
# default web port 9090
WEB_PORT=9101

PID_FILE=pid.node_exporter
LOG_FILE=log.node_exporter

echo node_exporter starting ...
nohup ./node_exporter --web.listen-address=:$WEB_PORT > $LOG_FILE 2>&1 & echo $! > $PID_FILE

echo node_exporter started on web : http://localhost:$WEB_PORT/
```
- 编写停止脚本
```shell
vi stop.sh
```
```shell
_p_pid=

PID_FILE=pid.node_exporter
PROCESS_NAME=node_exporter

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
- 启动
```shell
./start.sh
```
- 浏览器访问
```shell
http://localhost:9101/metrics
```
- 将实例添加到prometheus中
- 编辑prometheus配置文件
```shell
vi prometheus.yml
```
- 在 scrape_configs 节点中添加
```yml
scrape_configs:
  # ...
  - job_name: "node_exporter"
      static_configs:
        - targets: ["localhost:9101"]
```
- 保存后，重启prometheus即可


----------------------------------------------------------------------------

### Redis监控(redis_exporter)
- 需要配置被监控的Redis的连接信息
- 可以统计Redis的状态信息
- 地址
```shell
https://github.com/oliver006/redis_exporter/releases
```
- 下载
```shell
wget https://github.com/oliver006/redis_exporter/releases/download/v1.66.0/redis_exporter-v1.66.0.linux-amd64.tar.gz
```
- 解压
```shell
tar -xzvf redis_exporter-v1.66.0.linux-amd64.tar.gz
```
- 重命名
```shell
mv redis_exporter-v1.66.0.linux-amd64 redis_exporter-v1.66.0
```
- 进入路径
```shell
cd redis_exporter-v1.66.0
```
- 创建密码文件
```shell
vi password.cnf
```
```shell
xxx123456
```
- 编辑启动脚本
```shell
vi start.sh
```
```shell
# default web port 9090
WEB_PORT=9102

REDIS_ADDR=redis://localhost:6379
REDIS_PASSWORD=./password.cnf

PID_FILE=pid.redis_exporter
LOG_FILE=log.redis_exporter

echo node_exporter starting ...
nohup ./redis_exporter --redis.addr=$REDIS_ADDR --redis.password-file=$REDIS_PASSWORD --web.listen-address=:$WEB_PORT > $LOG_FILE 2>&1 & echo $! > $PID_FILE

echo redis_exporter started on web : http://localhost:$WEB_PORT/
```
- 编写停止脚本
```shell
vi stop.sh
```
```shell
_p_pid=

PID_FILE=pid.redis_exporter
PROCESS_NAME=redis_exporter

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
- 启动
```shell
./start.sh
```
- 浏览器访问
```shell
http://localhost:9102/metrics
```
- 将实例添加到prometheus中
- 编辑prometheus配置文件
```shell
vi prometheus.yml
```
- 在 scrape_configs 节点中添加
```yml
scrape_configs:
  # ...
  - job_name: "redis_exporter"
      static_configs:
        - targets: ["localhost:9102"]
```
- 保存后，重启prometheus即可


----------------------------------------------------------------------------

### MySQL监控(mysqld_exporter)
- 需要配置被监控的数据库的连接信息
- 可以统计数据库的状态信息
- 地址
```shell
https://prometheus.io/download/#mysqld_exporter
```
- 下载
```shell
wget https://github.com/prometheus/mysqld_exporter/releases/download/v0.16.0/mysqld_exporter-0.16.0.linux-amd64.tar.gz
```
- 解压
```shell
tar -xzvf mysqld_exporter-0.16.0.linux-amd64.tar.gz
```
- 重命名
```shell
mv mysqld_exporter-0.16.0.linux-amd64 mysqld_exporter-0.16.0
```
- 链接数据库，先添加一个用户，专用于检测
- 进入mysql命令行
```shell
mysql -u root -p
```
- 切换到mysql数据库
```sql
use mysql
```
```sql
CREATE USER 'mysql_exporter'@'localhost' IDENTIFIED BY 'xxx123456' WITH MAX_USER_CONNECTIONS 3;
GRANT PROCESS, REPLICATION CLIENT, SELECT ON *.* TO 'mysql_exporter'@'localhost';
```
- 退出mysql客户端
```sql
exit
```
- 进入路径
```shell
cd mysqld_exporter-0.16.0
```
- 添加数据库用户配置文件
```shell
vi my.cnf
```
```shell
[client]
user=mysql_exporter
password=xxx123456
```
- 编辑启动脚本
```shell
vi start.sh
```
```shell
# default web port 9090
WEB_PORT=9103

MYSQL_ADDRESS=localhost:3306
MYSQL_CONF=./my.cnf

PID_FILE=pid.mysqld_exporter
LOG_FILE=log.mysqld_exporter

echo mysqld_exporter starting ...
nohup ./mysqld_exporter --mysqld.address=$MYSQL_ADDRESS --config.my-cnf=$MYSQL_CONF --web.listen-address=:$WEB_PORT > $LOG_FILE 2>&1 & echo $! > $PID_FILE

echo mysqld_exporter started on web : http://localhost:$WEB_PORT/
```
- 编写停止脚本
```shell
vi stop.sh
```
```shell
_p_pid=

PID_FILE=pid.mysqld_exporter
PROCESS_NAME=mysqld_exporter

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
- 启动
```shell
./start.sh
```
- 浏览器访问
```shell
http://localhost:9103/metrics
```
- 将实例添加到prometheus中
- 编辑prometheus配置文件
```shell
vi prometheus.yml
```
- 在 scrape_configs 节点中添加
```yml
scrape_configs:
  # ...
  - job_name: "mysqld_exporter"
      static_configs:
        - targets: ["localhost:9103"]
```
- 保存后，重启prometheus即可


----------------------------------------------------------------------------

### MongoDB监控(mongodb_exporter)
- 需要配置被监控的MongoDB的连接信息
- 可以统计MongoDB的状态信息
- 地址
```shell
https://github.com/percona/mongodb_exporter/releases
```
- 下载
```shell
wget https://github.com/percona/mongodb_exporter/releases/download/v0.42.0/mongodb_exporter-0.42.0.linux-amd64.tar.gz
```
- 解压
```shell
tar -xzvf mongodb_exporter-0.42.0.linux-amd64.tar.gz
```
- 重命名
```shell
mv mongodb_exporter-0.42.0.linux-amd64 mongodb_exporter-0.42.0
```

----------------------------------------------------------------------------

### 黑盒网络监控(blackbox_exporter)
- 可以配置在任意主体上，针对目标主体的网络状态进行检测
- 主要统计网络状态信息
- 地址
```shell
https://prometheus.io/download/#blackbox_exporter
```
- 下载
```shell
wget https://github.com/prometheus/blackbox_exporter/releases/download/v0.25.0/blackbox_exporter-0.25.0.linux-amd64.tar.gz
```
- 解压
```shell
tar -xzvf blackbox_exporter-0.25.0.linux-amd64.tar.gz
```
- 重命名
```shell
mv blackbox_exporter-0.25.0.linux-amd64 blackbox_exporter-0.25.0
```

----------------------------------------------------------------------------

### ElasticSearch监控(elasticsearch_exporter)
- 需要配置被监控的ElasticSearch的连接信息
- 可以统计ElasticSearch的状态信息
- 地址
```shell
https://github.com/prometheus-community/elasticsearch_exporter/releases
```
- 下载
```shell
wget https://github.com/prometheus-community/elasticsearch_exporter/releases/download/v1.8.0/elasticsearch_exporter-1.8.0.freebsd-amd64.tar.gz
```
- 解压
```shell
tar -xzvf elasticsearch_exporter-1.8.0.freebsd-amd64.tar.gz
```
- 重命名
```shell
mv elasticsearch_exporter-1.8.0.freebsd-amd64 elasticsearch_exporter-1.8.0
```

----------------------------------------------------------------------------

### RabbitMQ监控(rabbitmq_exporter)
- 需要配置被监控的RabbitMQ的连接信息
- 可以统计RabbitMQ的状态信息
- 地址
```shell
https://github.com/kbudde/rabbitmq_exporter/releases
```
- 下载
```shell
wget https://github.com/kbudde/rabbitmq_exporter/releases/download/v1.0.0/rabbitmq_exporter_1.0.0_linux_amd64.tar.gz
```
- 解压
```shell
tar -xzvf rabbitmq_exporter_1.0.0_linux_amd64.tar.gz
```
- 重命名
```shell
mv rabbitmq_exporter_1.0.0_linux_amd64 rabbitmq_exporter_1.0.0
```

----------------------------------------------------------------------------

### Kafka监控(rabbitmq_exporter)
- 需要配置被监控的Kafka的连接信息
- 可以统计Kafka的状态信息
- 地址
```shell
https://github.com/danielqsj/kafka_exporter/releases
```
- 下载
```shell
wget https://github.com/danielqsj/kafka_exporter/releases/download/v1.8.0/kafka_exporter-1.8.0.freebsd-amd64.tar.gz
```
- 解压
```shell
tar -xzvf kafka_exporter-1.8.0.freebsd-amd64.tar.gz
```
- 重命名
```shell
mv kafka_exporter-1.8.0.freebsd-amd64 kafka_exporter-1.8.0
```

----------------------------------------------------------------------------

### Oracle监控(oracledb_exporter)
- 需要配置被监控的Oracle的连接信息
- 可以统计Oracle的状态信息
- 地址
```shell
https://github.com/iamseth/oracledb_exporter/releases
```
- 下载
```shell
wget https://github.com/iamseth/oracledb_exporter/releases/download/0.6.0/oracledb_exporter.tar.gz
```
- 解压
```shell
tar -xzvf oracledb_exporter.tar.gz
```
- 重命名
```shell
mv oracledb_exporter oracledb_exporter-0.6.0
```

----------------------------------------------------------------------------

### Postgres监控(postgres_exporter)
- 需要配置被监控的Postgres的连接信息
- 可以统计Postgres的状态信息
- 地址
```shell
https://github.com/prometheus-community/postgres_exporter/releases/
```
- 下载
```shell
wget https://github.com/prometheus-community/postgres_exporter/releases/download/v0.16.0/postgres_exporter-0.16.0.freebsd-amd64.tar.gz
```
- 解压
```shell
tar -xzvf postgres_exporter-0.16.0.freebsd-amd64.tar.gz
```
- 重命名
```shell
mv postgres_exporter-0.16.0.freebsd-amd64 postgres_exporter-0.16.0
```