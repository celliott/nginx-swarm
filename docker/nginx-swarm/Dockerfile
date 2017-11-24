FROM python:2.7-alpine

RUN apk add --update \
    ca-certificates \
    nginx \
    apache2-utils \
    certbot \
  && rm -rf /var/cache/apk/*

COPY config/supervisord.conf /etc/supervisord.conf

COPY config/nginx.conf /etc/nginx/nginx.conf
COPY config/default.conf /etc/nginx/conf.d/default.conf
COPY config/ssl.conf /etc/nginx/snippets/ssl.conf

WORKDIR /opt/app

ADD src/requirements.txt .
RUN pip install -r ./requirements.txt

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

ADD src .
RUN chmod +x *py

ENTRYPOINT ["/docker-entrypoint.sh"]
