FROM xmig/shellinabox_base
WORKDIR /

RUN yum install epel-release -y && \
    yum update -y && \
    yum install -y gcc \
        openssl-devel \
        bzip2-devel \
        libffi-devel \
        python36-pip.noarch \
        python36-devel \
        python-devel \
        python-pip \
        python-psutil \
        python-setuptools \
        python36-setuptools \
        nginx


ADD websshmanager/ /websshmanager
ADD config/ /websshmanager/config

RUN for file in \
  /etc/nginx/nginx.conf /etc/nginx/conf.d/nginx.vh.default.conf /etc/supervisord.conf; \
  do rm -fr $file; done

RUN ln -sF /websshmanager/config/nginx.conf /etc/nginx/nginx.conf
RUN ln -sF /websshmanager/config/supervisord.conf /etc/supervisord.conf

RUN for dir in  /var/log/nginx /var/lib/nginx ; \
  do mkdir -p $dir; chmod -R g+rwx $dir; chgrp -R root $dir; done

WORKDIR /websshmanager

RUN pip3 install -r /websshmanager/requirements.txt
RUN mkdir pids
RUN mkdir /.ssh

EXPOSE  7000
ENTRYPOINT ["./entrypoint.sh"]
