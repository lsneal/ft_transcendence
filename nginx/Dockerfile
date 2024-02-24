FROM alpine:3.18

RUN apk --update add --no-cache nginx

RUN apk add --no-cache autoconf \
						openrc \
						pkgconf \ 
						libcurl \
						automake \
						curl-dev \
						flex \
						g++ \
						gcc \
						geoip-dev \
						git \
						libc-dev \
						libmaxminddb-dev \
						libstdc++ \
						libtool \
						libxml2-dev \
						linux-headers \
						lmdb-dev \
						zlib-dev \
						make \
						gnupg \
						openssl-dev \
						pcre-dev \
						libxslt-dev \
						gd-dev \
						yajl-dev \
						perl-dev \
						yajl \
						bison \
						musl-dev \
						libpcrecpp \
						lua5.2-dev

RUN apk --update add --no-cache openssl \
	&& openssl req -x509 -nodes -subj "/C=FR/O=My Company/CN=example.com" -newkey rsa:2048 -keyout /etc/nginx/server.key -out /etc/nginx/server.crt \
	&& apk del openssl

WORKDIR /opt

RUN	wget https://nginx.org/download/nginx-1.24.0.tar.gz \
	&& git clone https://github.com/owasp-modsecurity/ModSecurity-nginx \
	&& git clone https://github.com/SpiderLabs/ModSecurity \
	&& tar -xvf nginx-1.24.0.tar.gz \
	&& rm -rf nginx-1.24.0.tar.gz

WORKDIR /opt/ModSecurity

RUN git submodule init \
	&& git submodule update \
	&& ./build.sh \
	&& ./configure \
	&& make \
	&& make install

WORKDIR /opt/nginx-1.24.0

RUN ./configure --add-dynamic-module=../ModSecurity-nginx --prefix=/var/lib/nginx --sbin-path=/usr/sbin/nginx --modules-path=/usr/lib/nginx/modules --conf-path=/etc/nginx/nginx.conf --pid-path=/run/nginx/nginx.pid --lock-path=/run/nginx/nginx.lock --http-client-body-temp-path=/var/lib/nginx/tmp/client_body --http-proxy-temp-path=/var/lib/nginx/tmp/proxy --http-fastcgi-temp-path=/var/lib/nginx/tmp/fastcgi --http-uwsgi-temp-path=/var/lib/nginx/tmp/uwsgi --http-scgi-temp-path=/var/lib/nginx/tmp/scgi --with-perl_modules_path=/usr/lib/perl5/vendor_perl --user=nginx --group=nginx --with-threads --with-file-aio --without-pcre2 --with-http_ssl_module --with-http_v2_module --with-http_realip_module --with-http_addition_module --with-http_xslt_module=dynamic --with-http_image_filter_module=dynamic --with-http_geoip_module=dynamic --with-http_sub_module --with-http_dav_module --with-http_flv_module --with-http_mp4_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_auth_request_module --with-http_random_index_module --with-http_secure_link_module --with-http_degradation_module --with-http_slice_module --with-http_stub_status_module --with-http_perl_module=dynamic --with-mail=dynamic --with-mail_ssl_module --with-stream=dynamic --with-stream_ssl_module --with-stream_realip_module --with-stream_geoip_module=dynamic --with-stream_ssl_preread_module \
	&& make modules \
	&& cp objs/ngx_http_modsecurity_module.so /etc/nginx/modules

RUN git clone https://github.com/coreruleset/coreruleset /usr/local/modsecurity-crs \
	&& mv /usr/local/modsecurity-crs/crs-setup.conf.example /usr/local/modsecurity-crs/crs-setup.conf \
	&& mv /usr/local/modsecurity-crs/rules/REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf.example /usr/local/modsecurity-crs/rules/REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf

RUN mkdir /etc/nginx/modsec \
	&& cp /opt/ModSecurity/unicode.mapping /etc/nginx/modsec \
	&& cp /opt/ModSecurity/modsecurity.conf-recommended /etc/nginx/modsec/modsecurity.conf

COPY ./conf/modsecurity.conf /etc/nginx/modsec
COPY ./conf/main.conf /etc/nginx/modsec

COPY ./conf/nginx.conf /etc/nginx/nginx.conf
COPY ./conf/ /etc/nginx/conf/

CMD ["/usr/sbin/nginx", "-g", "daemon off;"]