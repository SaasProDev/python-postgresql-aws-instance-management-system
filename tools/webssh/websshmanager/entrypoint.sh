#!/bin/bash

set +x

if [ -f "/usr/share/nginx/html/favicon.ico" ]; then
    echo "Favicon already exists."
else
  echo "Coping default favicon..."
  cp /websshmanager/shellinabox/favicon.ico /usr/share/nginx/html/
fi

echo "START nginx"  && nginx
echo "START manager" && python3 web_ssh_manager.py
#exec tini -- make supervisor