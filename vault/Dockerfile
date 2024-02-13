FROM vault:1.13.3

RUN apk add --no-cache curl \
                        jq \
                        openssl
                        
COPY ./conf.json /vault/config/

COPY ./script.sh .
RUN chmod +x script.sh

COPY ./policies.hcl .

CMD ["sh", "script.sh"]