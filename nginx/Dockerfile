FROM owasp/modsecurity-crs:nginx-alpine

USER root

COPY ./certificat.sh /opt

RUN apk add py3-pip && pip install hvac && chmod +x /opt/certificat.sh
RUN pip install hvac

COPY ./conf_modsecurity/crs-setup.conf /opt/owasp-crs/crs-setup.conf
COPY ./conf_modsecurity/main.conf /etc/nginx/conf/main.conf
COPY ./conf_modsecurity/modsecurity.conf /etc/modsecurity.d/modsecurity.conf
COPY ./conf/nginx.conf /etc/nginx/nginx.conf
COPY ./conf/ /etc/nginx/conf/
COPY ./pki.py /opt

RUN rm /var/log/nginx/access.log
RUN rm /var/log/nginx/error.log

ENV MODSEC_AUDIT_LOG /var/log/nginx/access.log
ENV MODSEC_DEBUG_LOG /var/log/nginx/error.log

CMD ["sh", "/opt/certificat.sh"]