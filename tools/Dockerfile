FROM centos:7

WORKDIR /

ADD build_context/ .

# RUN export LANG=en_US.utf8 && export LC_ALL=en_US.utf8

RUN yum install epel-release -y && \
    yum update -y && \
    yum install -y gcc make gcc-c++ \
				   screen \
				   openssh-clients \
				   git \
				   python36-pip.noarch \
				   python36-devel \
				   postgresql-contrib \
				   postgresql-devel \
				   python-devel \
				   python-pip \
				   python-psutil \
				   python-psycopg2 \
				   python-setuptools \
				   python36-devel \
				   python36-setuptools \
				   rsync \
				   setools-libs \
				   vim \
				   openssh \
				   openssh-clients \
				   openssl-devel \
				   bash-completion-extras \
				   python36-psutil \
				   libvirt-devel \
				   curl \
				   curl-devel \
				   libxml2-devel \
				   krb5-devel \
				   bubblewrap \
				   nginx \
				   && \
	mkdir -p /venv && chmod g+w /venv && \
		pip3 install virtualenv flake8 && \
		python3 -m venv --system-site-packages /venv/ansible && \
		/venv/ansible/bin/pip3 install --ignore-installed -r requirements.txt && \
		/venv/ansible/bin/pip3 install django-webpack-loader && \
		/venv/ansible/bin/pip3 install django_compressor && \
		/venv/ansible/bin/pip3 install supervisor Twisted[http2,tls] && \
		UWSGI_PROFILE_OVERRIDE=ssl=true /venv/ansible/bin/pip3 install uwsgi -I --no-cache-dir


#	virtualenv -p python --system-site-packages /venv/ansible && \
#		/venv/ansible/bin/pip install --ignore-installed six packaging appdirs && \
#		/venv/ansible/bin/pip install --ignore-installed setuptools==36.0.1 && \
#		/venv/ansible/bin/pip install --ignore-installed pip==9.0.1

# FRONTEND
WORKDIR /ahome_devel

RUN curl -sL https://rpm.nodesource.com/setup_12.x | bash - && \
    yum install -y nodejs && \
    npm i -g @angular/cli

RUN yum install -y https://github.com/krallin/tini/releases/download/v0.18.0/tini_0.18.0.rpm

RUN /usr/bin/ssh-keygen -q -t rsa -N "" -f /root/.ssh/id_rsa

# RUN openssl req -nodes -newkey rsa:2048 -keyout /etc/nginx/nginx.key -out /etc/nginx/nginx.csr -subj "/C=FR/ST=France/L=Rueil-Malmaison/O=AHOME/OU=CaaS Development/CN=127.0.0.1"
# RUN openssl x509 -req -days 365 -in /etc/nginx/nginx.csr -signkey /etc/nginx/nginx.key -out /etc/nginx/nginx.crt

RUN localedef -c -i en_US -f UTF-8 en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

WORKDIR /ahome_devel

RUN for file in \
  /etc/nginx/nginx.conf /etc/nginx/conf.d/nginx.vh.default.conf /etc/supervisord.conf; \
  do rm -fr $file; done

RUN ln -sF /ahome_devel/tools/nginx.conf /etc/nginx/nginx.conf
RUN ln -sF /ahome_devel/tools/nginx.vh.default.conf /etc/nginx/conf.d/nginx.vh.default.conf

#RUN ln -sF /ahome_devel/tools/supervisord.conf /etc/supervisord.conf

RUN ln -sF /ahome_devel/tools/supervisord-sergii.conf /etc/supervisord.conf


# Pre-create things that we need to write to
RUN for dir in  /var/log/nginx /var/lib/nginx /.local; \
  do mkdir -p $dir; chmod -R g+rwx $dir; chgrp -R root $dir; done

RUN for file in \
  /ahome_devel/ahome.log /var/run/nginx.pid; \
  do touch $file; chmod -R g+rwx $file; chgrp -R root $file; done

# AZURE CA CERTIFICATE
# openssl s_client -connect management.azure.com:443 -showcerts
# echo |     openssl s_client -servername management.azure.com -connect management.azure.com:443 2>/dev/null |     openssl x509 -text
# export REQUESTS_CA_BUNDLE=$VIRTUAL_ENV/lib/python3.6/site-packages/certifi/cacert.pem

RUN cat /azure.pem >> /venv/ansible/lib/python3.6/site-packages/certifi/cacert.pem && \
    rm /azure.pem


EXPOSE 8043 8443 8001 8000 5000

VOLUME ["/ahome_devel"]

WORKDIR /ahome_devel


ENTRYPOINT ["/entrypoint.sh"]
CMD ["/bin/bash"]

