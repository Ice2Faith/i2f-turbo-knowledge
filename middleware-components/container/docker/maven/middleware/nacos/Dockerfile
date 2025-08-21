FROM openjdk:8-jre-slim

# 定义时区
ENV TZ=PRC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone

# 定义运行用户
ENV APP_HOME=/app
ENV APP_USER=app

RUN groupadd $APP_USER \
    && useradd $APP_USER -d $APP_HOME -g $APP_USER -c $APP_USER \
    && mkdir -p $APP_HOME  \
    && chown -R $APP_USER:$APP_USER $APP_HOME

WORKDIR $APP_HOME


# 维护者
MAINTAINER app


# 可选配置项
ENV SERVER_PORT=8848
ENV GRPC_CLIENT_PORT=9848
ENV GRPC_SERVER_PORT=9849
ENV JRAFT_PORT=7848
ENV PARAMS=""
ENV JVM_OPTS=""
ENV SPRING_ENV=@spring.env@

# 定义构建参数
ENV TAR_NAME="nacos-server-2.3.2.tar.gz"

# 添加资源
ADD assets/$TAR_NAME .
COPY assets/resources/ ./nacos/

WORKDIR $APP_HOME/nacos/bin

# 执行最终降权运行
RUN chown -R $APP_USER:$APP_USER $APP_HOME \
    && usermod -u 2770 $APP_USER

USER 2770
# 暴露端口
EXPOSE $SERVER_PORT
EXPOSE $GRPC_CLIENT_PORT
EXPOSE $GRPC_SERVER_PORT
EXPOSE $JRAFT_PORT


ENTRYPOINT ["sh","-c","java -Xms1g -Xmx1g -Xmn512m \
                         -XX:MetaspaceSize=128m -XX:MaxMetaspaceSize=320m \
                         -XX:+UseConcMarkSweepGC -XX:+UseCMSCompactAtFullCollection -XX:CMSInitiatingOccupancyFraction=70 -XX:+CMSParallelRemarkEnabled -XX:SoftRefLRUPolicyMSPerMB=0 -XX:+CMSClassUnloadingEnabled -XX:SurvivorRatio=8 \
                         -verbose:gc -XX:+PrintGCDetails -XX:+PrintGCDateStamps -XX:+PrintGCTimeStamps -XX:+UseGCLogFileRotation -XX:NumberOfGCLogFiles=10 -XX:GCLogFileSize=100M \
                          -Dnacos.standalone=true \
                          -Dnacos.member.list= \
                          -Dloader.path=../plugins \
                          -Dnacos.home=../ \
                          -Dspring.profiles.active=$SPRING_ENV \
                          -Dserver.port=$SERVER_PORT \
                          $JVM_OPTS \
                          -jar ../target/nacos-server.jar  \
                          --spring.config.additional-location=file:../conf/ \
                          --logging.config=../conf/nacos-logback.xml \
                          --server.max-http-header-size=524288 \
                          $PARAMS "]
