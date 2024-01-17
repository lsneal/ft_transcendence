FROM alpine:3.18

RUN apk --update add --no-cache nginx


RUN apk --update add --no-cache openssl \
	&& openssl req -x509 -nodes -subj "/C=FR/O=My Company/CN=example.com" -newkey rsa:2048 -keyout /etc/nginx/server.key -out /etc/nginx/server.crt \
	&& apk del openssl

COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./conf/ /etc/nginx/conf/

CMD ["/usr/sbin/nginx", "-g", "daemon off;"]
