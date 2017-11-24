#!/bin/sh
set -e

PROXY_AUTH_USER=${PROXY_AUTH_USER:-'admin'}

sed -i "s/SERVICE_NAME/$PROXY_SERVICE_NAME/g" /etc/nginx/nginx.conf

mkdir -p /run/nginx

htpasswd -b -c /etc/nginx/.htpasswd $PROXY_AUTH_USER $PROXY_AUTH_PASS

supervisord -n --configuration /etc/supervisord.conf

exec "$@"
