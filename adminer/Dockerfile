FROM alpine:3.18

RUN apk --update add --no-cache php php-fpm php-session php-mysqli musl php-pgsql

COPY ./adminer.sh /run/adminer.sh
COPY ./www.conf /etc/php81/php-fpm.d/www.conf

ENTRYPOINT ["/run/adminer.sh"]
