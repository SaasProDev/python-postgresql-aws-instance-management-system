PYTHON ?= python3
PYTHON_VERSION = $(shell $(PYTHON) -c "from distutils.sysconfig import get_python_version; print(get_python_version())")
SITELIB=$(shell $(PYTHON) -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

# NOTE: This defaults the container image version to the branch that's active
COMPOSE_TAG ?= $(GIT_BRANCH)
COMPOSE_HOST ?= $(shell hostname)

MANAGEMENT_COMMAND ?= python3 manage.py

VENV_BASE ?= /venv
SCL_PREFIX ?=
CELERY_SCHEDULE_FILE ?= /var/lib/ahome/beat.db

# DEV_DOCKER_TAG_BASE ?= gcr.io/ansible-tower-engineering
# Python packages to install only from source (not from binary wheels)
# Comma separated list
SRC_ONLY_PKGS ?= cffi,pycparser,psycopg2,twilio

# Determine appropriate shasum command
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Linux)
	SHASUM_BIN ?= sha256sum
endif
ifeq ($(UNAME_S),Darwin)
	SHASUM_BIN ?= shasum -a 256
endif

# Get the branch information from git
GIT_DATE := $(shell git log -n 1 --format="%ai")
DATE := $(shell date -u +%Y%m%d%H%M)

NAME ?= ahome
GIT_REMOTE_URL = $(shell git config --get remote.origin.url)


# Create Django superuser.
adduser:
	@if [ "$(VENV_BASE)" ]; then \
		. $(VENV_BASE)/ansible/bin/activate; \
	fi; \
	$(MANAGEMENT_COMMAND) createsuperuser

# Create database tables and apply any new migrations.
migrate:
	@if [ "$(VENV_BASE)" ]; then \
		. $(VENV_BASE)/ansible/bin/activate; \
	fi; \
	$(MANAGEMENT_COMMAND) migrate --noinput

# Create database tables and apply any new migrations.
fixtures:
	@if [ "$(VENV_BASE)" ]; then \
		. $(VENV_BASE)/ansible/bin/activate; \
	fi; \
	$(MANAGEMENT_COMMAND) loaddata users.json
	$(MANAGEMENT_COMMAND) loaddata core.json
	$(MANAGEMENT_COMMAND) loaddata account.json

# Run django commants for system bootstrapping.
djangocommands:
	@if [ "$(VENV_BASE)" ]; then \
		. $(VENV_BASE)/ansible/bin/activate; \
	fi; \
	$(MANAGEMENT_COMMAND) rabbit_init


# Run after making changes to the models to create a new migration.
dbchange:
	@if [ "$(VENV_BASE)" ]; then \
		. $(VENV_BASE)/ansible/bin/activate; \
	fi; \
	$(MANAGEMENT_COMMAND) makemigrations


supervisor:
	@if [ "$(VENV_BASE)" ]; then \
		. $(VENV_BASE)/ansible/bin/activate; \
	fi; \
	supervisord --pidfile=/tmp/supervisor_pid -n

collectstatic:
	@if [ "$(VENV_BASE)" ]; then \
		. $(VENV_BASE)/ansible/bin/activate; \
	fi; \
	mkdir -p ahome/public/static && mkdir -p frontend/static && $(PYTHON) manage.py collectstatic --clear --noinput > /dev/null 2>&1


celery:
	@if [ "$(VENV_BASE)" ]; then \
		. $(VENV_BASE)/ansible/bin/activate; \
	fi; \
	mkdir -p /tmp/celery/{run,log} && ./tools/celerystarter/celery_worker.py
	#mkdir -p /tmp/celery/{run,log} && celery -A ahome worker -l info -n worker.%%h


#     celery multi start worker1 -A ahome \
# 		  --pidfile="/tmp/celery/run/%n.pid" \
# 		  --logfile="/tmp/celery/log/%n%I.log"

#     celery -A ahome worker -l info -n worker.%%h
#     celery --app=ahome.celery:app worker --loglevel=INFO -n worker.%%h

celery-devel:
	@if [ "$(VENV_BASE)" ]; then \
		. $(VENV_BASE)/ansible/bin/activate; \
	fi; \
    mkdir -p /tmp/celery/{run,log} && watchmedo auto-restart --directory=./core/tasks/ --pattern=*.py --recursive  -- celery -A ahome worker -l info -n worker.%%h


celery_flower:
	@if [ "$(VENV_BASE)" ]; then \
		. $(VENV_BASE)/ansible/bin/activate; \
	fi; \
	mkdir -p /tmp/celery/{run,log} && celery -A ahome flower


uwsgi:
	@if [ "$(VENV_BASE)" ]; then \
		. $(VENV_BASE)/ansible/bin/activate; \
	fi; \
	uwsgi --socket 127.0.0.1:8050 --module=ahome.wsgi:application --home=/venv/ansible --chdir=/ahome_devel/ \
		--vacuum --processes=5 --master  --py-autoreload 1 --max-requests=1000 --pidfile=/tmp/ahome-master.pid --stats /tmp/stats.socket \
		--logformat "%(addr) %(method) %(uri) - %(proto) %(status)"


# uwsgi: collectstatic
# 	@if [ "$(VENV_BASE)" ]; then \
# 		. $(VENV_BASE)/ansible/bin/activate; \
# 	fi; \
#     uwsgi --socket 127.0.0.1:8050 --module=ahome.wsgi:application --home=/venv/ansible --chdir=/ahome_devel/ \
# 	    --vacuum --processes=5 --master  --py-autoreload 1 --max-requests=1000 --pidfile=/tmp/ahome-master.pid --stats /tmp/stats.socket \
# 	    --logformat "%(addr) %(method) %(uri) - %(proto) %(status)"

#     uwsgi -b 32768 --socket 127.0.0.1:8050 --module=ahome.wsgi:application --home=/venv/ansible --chdir=/ahome_devel/ \
# 	    --vacuum --processes=5 --harakiri=120 --master --no-orphans --py-autoreload 1 --max-requests=1000 --pidfile=/tmp/ahome-master.pid --stats /tmp/stats.socket \
# 	    --lazy-apps --logformat "%(addr) %(method) %(uri) - %(proto) %(status)"

#     --attach-daemon2 'cmd=celery multi start worker1 -A ahome -l info --pidfile=/tmp/%n.pid --logfile="/tmp/%n%I.log' \


#     	beat -A myapp --schedule /var/lib/celery/beat.db --loglevel=INFO

daphne:
	@if [ "$(VENV_BASE)" ]; then \
		. $(VENV_BASE)/ansible/bin/activate; \
	fi; \
	mkdir -p /run/daphne/ && daphne -b 127.0.0.1 -p 8051 -e ssl:8443:privateKey=/ahome_devel/ssl/ahome.key:certKey=/ahome_devel/ssl/ahome.pem -v 2 --access-log - --proxy-headers ahome.asgi:application
# 	mkdir -p /run/daphne/ && daphne -b 127.0.0.1 -p 8051 -e ssl:8443:privateKey=/ahome_devel/ssl/ahome.key:certKey=/ahome_devel/ssl/ahome.pem -v 3 -u /run/daphne/daphne.sock --access-log - --proxy-headers ahome.asgi:application
# 	daphne -b 127.0.0.1 -v2 --access-log - --proxy-headers -p 8051 ahome.asgi:application


# 	daphne -b 127.0.0.1 -v2 --access-log /tmp/daphne.log --proxy-headers -p 8051 -e ssl:8052:privateKey=/ahome_devel/ssl/ahome.key:certKey=/ahome_devel/ssl/ahome.pem ahome.asgi:application
# 	daphne -b 127.0.0.1 -p 8051 ahome.asgi:application
#   command=daphne -u /run/daphne/daphne%(process_num)d.sock --fd 0 --access-log - --proxy-headers ahome.asgi:application


runworker:
	@if [ "$(VENV_BASE)" ]; then \
		. $(VENV_BASE)/ansible/bin/activate; \
	fi; \
	$(PYTHON) manage.py runworker notifications
#  channels
#  notifications console


# Run the built-in development webserver (by default on http://localhost:8001).
# (by default on https://localhost:8043).
runserver-https:
	@if [ "$(VENV_BASE)" ]; then \
		. $(VENV_BASE)/ansible/bin/activate; \
	fi; \
	$(PYTHON) manage.py runserver_plus 0.0.0.0:8043 --cert-file /ahome_devel/ssl/ahome.pem --key-file /ahome_devel/ssl/ahome.key


runserver:
	@if [ "$(VENV_BASE)" ]; then \
		. $(VENV_BASE)/ansible/bin/activate; \
	fi; \
	$(PYTHON) manage.py runserver 0.0.0.0:8001



# Run to start the background task dispatcher for development.
dispatcher:
	@if [ "$(VENV_BASE)" ]; then \
		. $(VENV_BASE)/ansible/bin/activate; \
	fi; \
	$(PYTHON) manage.py run_dispatcher


# Run to start the zeromq callback receiver
receiver:
	@if [ "$(VENV_BASE)" ]; then \
		. $(VENV_BASE)/ansible/bin/activate; \
	fi; \
	$(PYTHON) manage.py run_callback_receiver

nginx:
	nginx -g "daemon off;"

nginx-reload:
	nginx -s reload

jupyter:
	@if [ "$(VENV_BASE)" ]; then \
		. $(VENV_BASE)/ansible/bin/activate; \
	fi; \
	$(MANAGEMENT_COMMAND) shell_plus --notebook

reports:
	mkdir -p $@


certificate-ca:
	@if [ "$(VENV_BASE)" ]; then \
		. $(VENV_BASE)/ansible/bin/activate; \
	fi; \
	openssl genrsa -des3 -out ssl/rootCA.key 2048 && \
	openssl req -x509 -new -nodes -key ssl/rootCA.key -sha256 -days 1024 -out ssl/rootCA.pem


# Run to start the background task dispatcher for development.
certificate:
	@if [ "$(VENV_BASE)" ]; then \
		. $(VENV_BASE)/ansible/bin/activate; \
	fi; \
	openssl req -out ssl/ahome.csr -newkey rsa:2048 -nodes -keyout ssl/ahome.key -config ssl/san.cnf && \
	openssl x509 -req -days 365 -in ssl/ahome.csr -CA ssl/rootCA.pem -CAkey ssl/rootCA.key -CAcreateserial -out ssl/ahome.pem -extfile ssl/v3.ext && \
	yes | cp -fr ssl/ahome.pem /etc/nginx/nginx.crt && \
	yes | cp -fr ssl/ahome.key /etc/nginx/nginx.key && \
	make nginx-reload


# Run to start the background task dispatcher for development.
docker-compose-build:
	cd tools/ && docker-compose build

# Run to start the background task dispatcher for development.
docker-compose-stop:
	cd tools/ && docker-compose stop

# Run to start the background task dispatcher for development.
docker-compose-refresh:
	cd tools/ && docker-compose stop && docker-compose rm --force

# Run to start the background task dispatcher for development.
docker-compose-clean:
	cd tools/ && docker-compose stop && docker-compose rm --force && docker volume rm tools_ahome_psql_data --force

# Run to start the background task dispatcher for development.
docker-compose-devel:
	cd tools/ && rsync -av supervisord-devel.conf supervisord.conf && docker-compose up


# Run to start the background task dispatcher for development.
docker-compose-prod:
	cd tools/ && rsync -av supervisord-prod.conf supervisord.conf && docker-compose up

# UI
node-install:
	export NODE_OPTIONS=--max_old_space_size=4096 && \
	cd ui/ && npm install

frontend-ui:
	export NODE_OPTIONS=--max_old_space_size=4096 && \
	cd ui/ && ng build --source-map=false --build-optimizer=false --deployUrl=/static/ && \
	rsync -a /ahome_devel/ui/dist/ui/* /ahome_devel/frontend/static/

frontend-serve:
	export NODE_OPTIONS=--max_old_space_size=4096 && \
	cd ui/ && ng serve --port 8043 --host 0.0.0.0 --watch --disableHostCheck



# socketio
socketio-uwsgi:
	@if [ "$(VENV_BASE)" ]; then \
		. $(VENV_BASE)/ansible/bin/activate; \
	fi; \
	uwsgi --http :5000 --gevent 1000 --http-websockets --master --wsgi-file /ahome_devel/socketio_app/wsgi.py --callable application \
		  --module=socketio_app.wsgi:application --home=/venv/ansible --chdir=/ahome_devel/ --env DJANGO_SETTINGS_MODULE=ahome.settings \
		  --vacuum --processes=5 --master  --py-autoreload 1 --max-requests=1000 --pidfile=/tmp/ahome.socketio.pid --stats /tmp/stats.socketio.socket \
		  --logformat "%(addr) %(method) %(uri) - %(proto) %(status)"



