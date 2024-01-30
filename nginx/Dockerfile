FROM alpine:3.18

RUN apk --update add --no-cache nginx
RUN mkdir -p /etc/nginx/certs

RUN apk --update add --no-cache openssl \
	&& openssl req -x509 -nodes -subj "/C=FR/O=My Company/CN=example.com" -newkey rsa:2048 -keyout /etc/nginx/certs/server.key -out /etc/nginx/certs/server.crt \
	&& apk del openssl

COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./conf/ /etc/nginx/conf/

CMD ["/usr/sbin/nginx", "-g", "daemon off;"]
