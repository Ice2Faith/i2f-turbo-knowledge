FROM nginx

ENV TZ=PRC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

MAINTAINER rwd

ENV SERVER_PORT=8080

ENV PARAMS=""

COPY dist/ /dist
COPY nginx.conf /etc/nginx/conf.d/default.conf

WORKDIR /

EXPOSE $SERVER_PORT

ENTRYPOINT ["sh","-c","nginx -g 'daemon off;' $PARAMS"]
