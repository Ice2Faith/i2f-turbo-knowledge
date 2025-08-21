FROM nginx:alpine

# 定义时区
ENV TZ=PRC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone

# 定义运行用户
ENV APP_HOME=/app
ENV APP_USER=app

RUN addgroup -S -g 2779 $APP_USER \
  ; adduser -S -G $APP_USER -u 2770 $APP_USER \
  ; mkdir -p $APP_HOME \
  ; chown -R $APP_USER:$APP_USER $APP_HOME

WORKDIR $APP_HOME


# 维护者
MAINTAINER app


# 可选配置项
ENV SERVER_PORT=8080
ENV PARAMS=""

# 添加资源
COPY dist ./dist
COPY nginx-@build.env@.conf /etc/nginx/nginx.conf


RUN mkdir -p /var/cache/nginx && chown -R $APP_USER:$APP_USER /var/cache/nginx && chmod -R 777 /var/cache/nginx && \
    mkdir -p /var/log/nginx  && chown -R $APP_USER:$APP_USER /var/log/nginx && chmod -R 777 /var/log/nginx && \
    mkdir -p /run/nginx  && chown -R $APP_USER:$APP_USER /run/nginx && chmod -R 777 /run/nginx && \
    mkdir -p /var/lib/nginx  && chown -R $APP_USER:$APP_USER /var/lib/nginx && \
    chown -R $APP_USER:$APP_USER /etc/nginx && chmod -R 777 /etc/nginx


# 执行最终降权运行
RUN chown -R $APP_USER:$APP_USER $APP_HOME

USER 2770

# 暴露端口
EXPOSE $SERVER_PORT

ENTRYPOINT ["sh","-c","nginx -g 'daemon off;master_process on;' $PARAMS"]
