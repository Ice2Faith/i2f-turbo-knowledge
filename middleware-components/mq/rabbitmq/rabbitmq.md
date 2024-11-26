# rabbit mq

- rabbitmq是由erlang编写的mq服务
- 因此使用时需要erlang环境
- 也就是需要先安装erlang
- 注意，rabbitmq因为是erlang环境
- 所以，rabbitmq的版本就需要特定的erlang版本对应才行
- 从下面地址从查找版本关系

```shell
https://www.rabbitmq.com/docs/which-erlang
```

## windows安装

### 安装erlang

- 前面说了，因为是使用erlang编写的
- 所以，需要先安装erlang环境
- 官网

```shell
https://www.erlang.org/
```

- 下载

```shell
https://github.com/erlang/otp/releases/download/OTP-24.0/otp_win64_24.0.exe
```

- 安装
- 双击安装即可，路径尽量不要包含空格和中文符号
- 我的安装路径如下

```shell
C:\erl-24.0
```

- 勾选要安装的内容时
- 全部勾选即可
- 配置环境变量

```shell
ERLANG_HOME
C:\erl-24.0

Path
%ERLANG_HOME%\bin
```

- 验证安装
- 打开cmd

```shell
erl -version
```

### 安装rabbitmq

- 官网

```shell
https://www.rabbitmq.com/
```

- 下载地址

```shell
https://github.com/rabbitmq/rabbitmq-server/releases
```

- 下载

```shell
https://github.com/rabbitmq/rabbitmq-server/releases/download/v3.9.5/rabbitmq-server-3.9.5.exe
```

- 安装
- 双击安装即可
- 需要勾选安装的组件时
- 全部勾选即可
- 安装配置管理项
- 进入安装目录

```shell
cd /sbin
```

- 启动管理插件

```shell
rabbitmq-plugins enable rabbitmq_management
```

- 检查服务状态

```shell
rabbitmqctl status
```

- 没有启动的话，可以自己启动一下

```shell
rabbitmq-server.bat
```

- 浏览器访问

```shell
http://localhost:15672
```

- 用户名密码

```shell
guest
guest
```

## Linux安装

### 安装erlang

- 前面说了，因为是使用erlang编写的
- 所以，需要先安装erlang环境
- 官网

```shell
https://www.erlang.org/
```

- 下载

```shell
https://github.com/erlang/otp/releases/download/OTP-24.0/otp_src_24.0.tar.gz
```

- 解压

```shell
tar -xzvf otp_src_24.0.tar.gz
```

- 进入路径

```shell
cd otp_src_24.0
```

- 编译并安装

```shell
./configure && make && make install
```

- 验证安装

```shell
erl -version
```

### 安装rabbitmq

- 官网

```shell
https://www.rabbitmq.com/
```

- 下载地址

```shell
https://github.com/rabbitmq/rabbitmq-server/releases
```

- 下载

```shell
https://github.com/rabbitmq/rabbitmq-server/releases/download/v3.9.5/rabbitmq-server-3.9.5.tar.xz
```

- 解压

```shell
tar -xzvf rabbitmq-server-3.9.5.tar.xz
```

- 进入路径

```shell
cd rabbitmq-server-3.9.5
```

- 安装配置管理项
- 进入安装目录

```shell
cd /sbin
```

- 启动管理插件

```shell
./rabbitmq-plugins.sh enable rabbitmq_management
```

- 检查服务状态

```shell
./rabbitmqctl.sh status
```

- 没有启动的话，可以自己启动一下

```shell
./rabbitmq-server.sh
```

- 浏览器访问

```shell
http://localhost:15672
```

- 用户名密码

```shell
guest
guest
```
