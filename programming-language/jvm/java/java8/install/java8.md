# java8 环境安装

## 简介
- java8是目前使用最多的jdk版本

## 依赖环境
- 无

## 安装
- 检查yum
```shell script
yum list java*
```
- 安装
```shell script
yum -y install java-1.8.0-openjdk*
```
- 验证
```shell script
java -version
```

## 方式二
- 下载
```shell script
wget https://download.java.net/openjdk/jdk8u42/ri/openjdk-8u42-b03-linux-x64-14_jul_2022.tar.gz
```
- 解包
```shell script
tar -xzvf openjdk-8u42-b03-linux-x64-14_jul_2022.tar.gz
```
- 进入包
```shell script
cd openjdk-8u42-b03-linux-x64-14_jul_2022
```
- 复制路径
```shell script
pwd
```
- 添加环境变量
```shell script
vi /etc/profile
```
- 末尾添加以下配置
```shell script
export JAVA_HOME=
export CLASSPATH=.:$JAVA_HOME/jre/lib/rt.jar:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
export PATH=$PATH:$JAVA_HOME/bin
```
- 退出并保存
- 重新应用环境变量
```shell script
source /etc/profile
```
- 验证环境
```shell script
java -version
```