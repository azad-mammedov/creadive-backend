#!/bin/sh
set -e

CONF="/etc/nginx/nginx.conf"

if [ ! -f "/etc/letsencrypt/live/backend.creadive.az/fullchain.pem" ]; then
    echo "No SSL certificates found – starting Nginx in HTTP-only mode"
    # Comment out the entire HTTPS server block
    sed -i '/listen 443 ssl/,/}/s/^/#/' $CONF
    sed -i '/ssl_certificate/d' $CONF
    sed -i '/ssl_certificate_key/d' $CONF
else
    echo "SSL certificates found – enabling HTTPS"
    # Uncomment if you commented them before (optional)
    sed -i '/listen 443 ssl/,/}/s/^#//' $CONF || true
fi

exec nginx -g "daemon off;"