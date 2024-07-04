# docker usage
---
## intro
- docker 依赖于Linux内核，因此要运行docker就必须要有一个Linux内核
- 什么是Linux内核？和常说的Linux系统什么关系？
- Linux kernel(linux内核)是Linux系统的核心
- 提供了最基本的内核管理（作业调度、进程调度、网络调度、文件调度等）
- 在其基础上，推展除了各种Linux发行版（redhat,centos,deepin,ubuntu...）
- 也就是说，centos系统=Linux内核+centos发行版
- 类比来说：
- android 系统，提供了最核心的功能
- 其他android开发商基于android拓展出了flyme,miui,colorOs...
- docker 通过Linux内核提供的隔离能力
- 采用多层文件系统，分离出每一层
- 最底层，当然是Linux内核
- 一般的第二次就是一个Linux发行版
- 下面依次叠加更高的层
## docker的分层
- 首选举个例子来看一下
- 0.linux内核层（操作系统提供，docker共享内核）
- 1.centos发行版（docker提供，借助共享的内核）
- 2.jdk/jre/jvm层（docker提供，用于提供java开发或运行的环境）
- 3.tomcat层（docker提供，用于运行java的web程序）
- 4.web程序层（用户提供，将其放入上一层的tomcat中运行）
- 每一层，都是独立的层，也就是如此
- 在docker镜像下载时，会分别下载每一层
- 如果本地已经存在这一层了，那么直接使用，不再重复下载
- 也就是如此，每一层只需要下载一次
- 所以，就算docker镜像看起来那么大，但是实际上，重复的层是复用的
- 实际占用空间并没有那么大
## 固件层和读写层
- 上面的例子中，是一个典型的场景，每一层都依赖于上一层的基础运行
- 其中0-3层可以是一个固定的镜像层，不需要进行改动
- 而，第4层则是用户自己进行交互的层
- 但是，不可避免的会遇到需要修改底层参数的情况，例如修改tomcat配置，修改centos配置等
- 这些修改都不会直接修改底层固有的配置
- 底层的配置都是只读的
- docker采用了分层的方式，将每一层的修改记录保存下来，在运行时覆盖的方式，达到可以修改
- 对于特殊的，删除配置文件这些方式，也是作为修改记录保存下来，这样的被标记为删除，运行时不再加载
- 因此，镜像是固定的，而镜像运行生成的容器示例是可变的

---
## docker的基本操作
### 安装docker
- 这部分比较简单，如果是centos7,提供了一份脚本，在./install/centos7/docker-install.sh
- 按照脚本执行即可

### docker的运行原理
- 可以参考git的使用原理
- 在dockerhub中search需要的镜像
```perl
docker search nginx
```
- 将需要的镜像pull到本地
```perl
docker pull nginx
```
- 检查本地有哪些镜像images
```perl
docker images
```
- 运行一个指定的镜像run生成一个容器container
- 参数解析
    - -d 指定为后台运行
    - --rm 指定运行结束之后，删除容器，注意是容器，而不是镜像
    - -it 提供一个交互式的终端-i,-t
    - -p 指定将主机的8080端口映射到容器的80端口
    - -v 指定将主机的/data/nginx映射为容器的/data
    - nginx 镜像名称
    - /bin/bash 进入容器后运行的命令
- 因此，这条命令就是运行nginx，并以终端进入，使用的bash终端
- 同时，需要注意的是，容器内必须有一个前台进程在运行，否则容器会自动关闭
```perl
docker run -d --rm -it -p 8080:80 -v /data/nginx:/data nginx /bin/bash
```
- 最简单的后台运行方式
```perl
docker run -d nginx
```
- 最简单的方式
```perl
docker run nginx
```
- 其他的启动参数
    - --name 指定容器名称，在ps中更好看
    - -P 大P表示随机端口映射
    - -p :80 将容器中的80端口随机映射到主机端口
- 查看正在运行的容器ps
```perl
docker ps
```
- 对于已经关闭的容器，查看需要带上-a参数
```perl
docker ps -a
```
- 进入一个正在运行的容器exec
    - 使用docker ps之后，会方辉container id容器ID
    - 在后续对容器进行操作都是基于这个容器ID的
    - 容器ID完整的是SHA256的值，ps显示的是前面的一部分
    - 但是基于操作上来说，一般使用容器ID的前3位即可
    - 其他的参数，和run基本一致
    - 一般来说，进入容器是想要进行操作的，因此指定-it和指定一个终端bash/sh是必要的
```perl
docker exec -it 容器ID bash
```
- 停止指定的容器stop
```perl
docker stop 容器ID
```
- 删除指定的容器rm
    - 在镜像还有使用他的容器时，镜像不允许删除
```perl
docker rm 容器ID
```
- 删除指定的镜像rmi
```perl
docker rmi 镜像名称
```
- 提交自己对镜像的修改commit
    - 将容器中的修改提交成为一个镜像
    - 通过-t指定镜像名称，否则默认只有容器ID，在docker images中
```perl
docker commit 容器ID -t 镜像名称
```
- 保存自己的镜像save
```perl
docker save 镜像名称 -o 保存的镜像文件名
```
- 载入别人分享的镜像load
```perl
docker load -i 加载的镜像文件名称
```
- 同时，你也可以在dockerhub上注册自己的账号，将自己创建的镜像，提交到远程
- 这里不给出

### Dockerfile 自定义镜像
- 上面说了，可以使用commit+save+load方式实现自定义镜像
- 但是这种操作可能还是比较麻烦
- 因此，借助Dockerfile就能够生成一个镜像
- 使用上类似Makefile
- 在Dockerfile所在路径执行docker build .即可
- Dockerfile因为docker的分层原理，因此也是根据层进行的
- 使用上类似maven，需要指定一个FROM，也就是基本层parent
- 至少有一个FROM，毕竟至少得有一个Linux发型版吧，特殊情况除外
- 几个主要组成部分
    - FROM 制定一个父镜像
    - RUN 执行一个Linux命令
    - COPY 将主机中的文件拷贝到容器中
    - CMD 指定要运行的程序或者命令
        - 当ENTRYPOINT指定时，退化为ENTRYPOINT的参数
        - 同时CMD能够在容器运行时，被运行参数覆盖，因此可以作为默认参数使用
    - ENTRYPOINT 指定容器的入口点，也就是要运行的程序或命令
- 下面给出一个，运行指定jar包的Dockerfile的编写内容
```perl
# 指定父层，为一个具有openjdk8的基础层，因此，这一步就已经具有java8的环境了
FROM openjdk:8-jdk-alpine

# 在主机中用一个匿名的文件夹挂载为容器中的/tmp
VOLUME /tmp

# 将主机中的app.jar拷贝到容器中的/apps/app.jar
COPY app.jar /apps/app.jar

# 这里同时指定了CMD和ENTRYPOINT，因此CMD退化为ENTRYPOINT的参数
CMD ["--boot.env=docker"]

# 容器的入口点，因此在容器启动时，就运行了这条命令
ENTRYPOINT ["java","-jar","/apps/app.jar"]

```
- 因此这个容器默认启动运行的命令为：
```perl
java -jar /apps/app.jar --boot.ent=docker
```
- 又因为，CMD能够被启动参数覆盖
- 假定启动命令为
```perl
docker run -d --rm test-jar-img --server.port=8080
```
- 则实际执行的命令是
```perl
java -jar /apps/app.jar --server.port=8080
```
- 现在Dockerfile文件编写好了
- 主要注意的是，Dockerfile的这个文件名，必须是这个，大小写也要一致
- 除非某些Linux对于文件大小写文件名不敏感，则大小写可以不一致
- 为了保证纯净，单独放到一个干净的文件夹中
- 另外，Dockerfile中，指定了，需要一个app.jar
- 这里随便准备一个springboot的jar
- 一并放进去
```perl
/jar8env
    Dockerfile
    app.jar
```
- 进入此路径并构建得到镜像
```perl
cd jar8env
docker build . -t test-jar-img
```
- 这样，就得到了一个叫做test-jar-img的镜像
- 可以在镜像中看到
```perl
docker images
```
- 现在就可以运行这个镜像了
- 指定CMD镜像覆盖，从而指定了端口，同时将主机的80端口，映射为容器的8080端口
- 为了方便查看，并未指定-d后台运行，因此，这里就直接可以看到springboot的启动日志了，并且也在8080端口启动了
- 由于指定了--rm,因此在终止运行之后，容器也随之删除
- 如果想要验证端口映射，则加上-d后台运行，然后通过docker ps 查看端口映射信息
```perl
docker run --rm -p 80:8080 test-jar-img --server.port=8080
```

## 完结
- 基础的docker使用和Dockerfile的编写及构建，就已经结束了
- 部分基础参考在jar8env文件夹下面给出
- 剩下的就可以自行探索更高级的使用方式
- 基于docker构建集群，结合k8s做容器编排
