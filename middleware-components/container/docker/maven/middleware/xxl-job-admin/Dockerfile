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
ENV SERVER_PORT=8080
ENV PARAMS=""
ENV JVM_OPTS=""
ENV SPRING_ENV=@spring.env@
ENV LOGBACK_ENV=@logback.env@

# 定义构建参数
ENV APP_NAME="xxl-job-admin"
ENV TAR_NAME="${APP_NAME}-all.tar.gz"
ENV JAR_NAME="${APP_NAME}.jar"

# 添加资源
ADD assets/$TAR_NAME .
COPY assets/resources/* ./$APP_NAME/resources/

WORKDIR $APP_HOME/$APP_NAME

# 执行最终降权运行
RUN chown -R $APP_USER:$APP_USER $APP_HOME \
  && usermod -u 2770 $APP_USER

USER 2770
# 暴露端口
EXPOSE $SERVER_PORT
ENTRYPOINT ["sh","-c","java -jar -Dlogback.app.env=$LOGBACK_ENV -Dspring.profiles.active=$SPRING_ENV -Dserver.port=$SERVER_PORT $JVM_OPTS $JAR_NAME $PARAMS"]
