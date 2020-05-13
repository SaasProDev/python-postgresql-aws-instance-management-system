#!/bin/bash

echo "**** CORE CONTAINER STARTING... ****"
set +x

#ENTRYPOINT ["python3", "manage.py", "runserver", "0.0.0.0:8001"]

# Move to the source directory so we can bootstrap
if [ -f "/ahome_devel/manage.py" ]; then
    cd /ahome_devel
else
    echo "Failed to find ahome source tree, map your development tree volume"
fi

while ! nc -z rabbitmq 5672;
do
  echo Waiting for rabbitmq service start...;
  sleep 1;
done;
# echo Waiting Rabbit really UP...
# sleep 2;
echo Rabbitmq connected!;

source /venv/ansible/bin/activate
#pip3 freeze

echo "APPLY migrate"  && make migrate
echo "APPLY FIXTURES" && make fixtures
echo "APPLY COMMANDS" && make djangocommands

#make migrate
#make fixtures
#make node-install
#make frontend-ui
# make collectstatic
# make init


# source /venv/ansible/bin/activate; \

# python3 manage.py runserver 0.0.0.0:8001

# exec $@


cd /ahome_devel
# Start the services
exec tini -- make supervisor