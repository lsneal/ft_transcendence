FROM vault:1.13.3

RUN apk add --no-cache curl \
                        jq \
                        openssl
                        
COPY ./conf/conf.json /vault/config/

COPY ./script.sh .
RUN chmod +x script.sh

COPY ./policies/policies_users.hcl .
COPY ./policies/policies_pong.hcl .
COPY ./policies/policies_nginx.hcl .

CMD ["./script.sh"]