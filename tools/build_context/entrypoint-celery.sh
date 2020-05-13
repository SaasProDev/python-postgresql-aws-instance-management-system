#!/bin/bash

echo "**** CELERY CONTAINER STARTING... ****"

set +x

if [ -f "/ahome_devel/manage.py" ]; then
    cd /ahome_devel
else
    echo "Failed to find awx source tree, map your development tree volume"
fi

while ! nc -z rabbitmq 5672;
do
  echo Waiting for rabbitmq service start...;
  sleep 1;
done;
echo Rabbitmq connected!;

source /venv/ansible/bin/activate


cd /ahome_devel
# Start the services
#exec tini -- make supervisor
make celery-devel
