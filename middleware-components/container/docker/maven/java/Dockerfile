FROM openjdk:8-jre-slim

ENV TZ=PRC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

MAINTAINER rwd

ENV JAR_NAME="rwd-gateway.jar"
ENV SERVER_PORT=8080

ENV SPRING_ENV=@spring.env@
ENV LOGBACK_ENV=@logback.env@

ENV PARAMS=""
ENV JVM_OPTS=""

ADD target/$JAR_NAME /

WORKDIR /

EXPOSE $SERVER_PORT

ENTRYPOINT ["sh","-c","java -jar $JAVA_OPTS -Dlogback.app.env=$LOGBACK_ENV -Dspring.profiles.active=$SPRING_ENV -Dserver.port=$SERVER_PORT  $JVM_OPTS $JAR_NAME $PARAMS"]
