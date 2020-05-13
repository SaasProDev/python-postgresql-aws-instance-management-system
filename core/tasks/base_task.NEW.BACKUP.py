import errno
import functools
import os
import re
import shutil
import stat
import tempfile
import time
import traceback

import uuid
import copy
import netaddr

from distutils.dir_util import copy_tree
from distutils.version import LooseVersion as Version
import yaml
import fcntl
try:
    import psutil
except Exception:
    psutil = None


from slugify import slugify, Slugify, UniqueSlugify

from pprint import pprint, pformat


def nice_format(data):
    return pformat(data, indent=4).encode("UTF-8")


# Celery

from celery import Celery
from celery import Task, shared_task
from celery.signals import celeryd_init, worker_shutdown
from celery.utils.log import get_task_logger
from celery.schedules import crontab
from celery_progress.backend import ProgressRecorder

from celery import states
from celery.exceptions import Ignore
from celery import chain



# Django
from django.conf import settings
from django.db import transaction, DatabaseError, IntegrityError
from django.db.models.fields.related import ForeignKey
from django.utils.timezone import now, timedelta
from django.utils.encoding import smart_str
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize

from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.apps import apps
from django.apps import AppConfig

# Channels
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Django DRF
from rest_framework.exceptions import PermissionDenied


from core.models import * #noqa


from core.utils import get_model_from_str, load_yml_to_dict, ahomefile_to_dict, dict_yaql, append_ahomefile_fields, ahomefile_yaql, get_ssh_version


import yaml
import ansible_runner

from random import randrange

# #The decorator is used for recognizing a periodic task
# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):

#     #Sending the email every 10 Seconds
#     sender.add_periodic_task(10.0, send_feedback_email_task.s('Ankur','ankur@xyz.com','Hello'), name='add every 10')
#   # Executes every Monday morning at 7:30 a.m.
#     sender.add_periodic_task(
#         crontab(hour=7, minute=30, day_of_week=1),
#         send_feedback_email_task.s('Ankur','ankur@xyz.com','Hello'),)


logger = get_task_logger(__name__)
import logging
logger = logging.getLogger(__name__)


app = Celery()
class Config:
    enable_utc = True
    timezone = 'Europe/Paris'

app.config_from_object(Config)


HIDDEN_PASSWORD = '**********'

OPENSSH_KEY_ERROR = u'''\
It looks like you're trying to use a private key in OpenSSH format, which \
isn't supported by the installed version of OpenSSH on this instance. \
Try upgrading OpenSSH or providing your private key in an different format. \
'''


DEVICE_TEMPLATES = ['device', 'virtualmachine', 'networkgear', 'container', ]




@shared_task(bind=True)
def my_task(self, seconds):
    progress_recorder = ProgressRecorder(self)
    for i in range(seconds):
        time.sleep(1)
        progress_recorder.set_progress(i + 1, seconds)
    return 'done'




def with_path_cleanup(f):
    @functools.wraps(f)
    def _wrapped(self, *args, **kwargs):
        try:
            return f(self, *args, **kwargs)
        finally:
            for p in self.cleanup_paths:
                try:
                    if os.path.isdir(p):
                        shutil.rmtree(p, ignore_errors=True)
                    elif os.path.exists(p):
                        os.remove(p)
                except OSError:
                    logger.exception("Failed to remove tmp file: {}".format(p))
            self.cleanup_paths = []
    return _wrapped


class BaseTask(Task):

    ignore_result = False
    validation_class = ''
    name = ''
    description = ''
    abstract = True

    model = None
    pk = None

    event_ct = 0
    event_total = 100
    task_id = None

    namespace = ''

    job_defaults = dict()

    notifications = dict()

    action = None


    # def __call__(self, *args, **kwargs):
    #     """In celery task this function call the run method, here you can
    #     set some environment variable before the run of the task"""

    #     # logger.info("Starting to run")



    #     return self.run(*args, **kwargs)


    def run(self, instance, **kwargs):

        # logger = self.get_logger(**kwargs)
        self.cleanup_paths = []

        self.model = instance.get('model')
        self.pk = instance.get('pk')
        instance = instance.get('fields')
        self.instance = instance

        self.namespace = self.get__namespace(instance)

        self.event_ct = 0
        self.event_total = 100

        self.action = kwargs.get("action", self.instance.get('action'))


        # logger.info("Starting to run")

        #progress bar
        # self.set__progress()

        self.task_id = kwargs.get("task_id", None)


        # logger.info('BaseTask task id {}'.format(kwargs.get("task_id", None)))

        # logger.info('BaseTask kwargs {}'.format(kwargs))

        self.notifications = dict(
                # group   = "notifications",
                alert  = "info",
                verb   = "starting",
                msg    = "",
            )

        self.emit__channel_notification()

        # self.emit__notification("notifications", "notification", "Job started", **kwargs)

        # self.emit__channel_notification(
        #         'inventories-status_changed',
        #         {'group_name': 'inventories', 'inventory_id': inventory_id, 'status': 'deleted'}
        #     )

        # logger.info("Execute every 0:15 past the hour every day.")

        #progress bar
        # self.set__progress()

        self.job_defaults = {
                'rc': None,
                'status': 'error',
                'stats': dict(),
                'namespace': self.namespace,
                'fail_msg': '',
                'celery_task_id': self.task_id,
                'celery_progress': 0,
                'celery_event_ct': 0,
                }


        private_data_dir = self.build__private_data_dir(instance)

        sshkey = self.build__sshkey(instance, private_data_dir)
        
        logger.info("sshkey: {}".format(sshkey))

        opts = copy.deepcopy(kwargs)
        opts.update(sshkey)

        # logger.info("kwargs: {}".format(kwargs))

        
        extravars =  self.build__extravars( instance, private_data_dir, dict() )
        
        # logger.info(extravars)

        envvars =  self.build__envvars(instance, private_data_dir, **opts)

        inventory = self.build__inventory(instance, private_data_dir, **opts)

        roles_path = self.build__roles(instance, private_data_dir, self.namespace)

        process_isolation_params = self.build__params_process_isolation(instance, private_data_dir, 'cwd')

        """
        Need a logic to determine based on inputs/instance what to do
        """
        '''
        'event_handler': self.event_handler,
        'cancel_callback': self.cancel_callback,
        'finished_callback': self.finished_callback,
        'status_handler': self.status_handler,
        '''

        runner_args = dict(
            private_data_dir = private_data_dir,
            directory_isolation_base_path = private_data_dir,
            json_mode = False,
            process_isolation = True,
            status_handler = self.status_handler,
            event_handler = self.event_handler,
            finished_callback = self.finished_callback,
        )

        runner_args.update(
            dict(
                role = self.namespace, 
                roles_path = roles_path,
            )
        )

        # process isolation
        runner_args.update(process_isolation_params)


        runner = ansible_runner.interface.run(**runner_args)

        # self.event_ct = len(runner.events)

        # save_job = self.save__job(instance)

        # job_events = self.event__dispatch(instance, self.namespace, runner)

        # successful: 0
        # logger.info("{}: {}".format(runner.status, runner.rc))
        # logger.info("Final status : \n{}".format(runner.stats))

        # save_job = self.save__job(instance)

        # self.emit__notification("notifications", "notification", "Job finished", **kwargs)

        # logger.info(f"Final runner output => \nstatus: {runner.status} rc: {runner.rc}")

        # logger.info(f"Final runner output : \n{runner.status}")

        return runner

    def set__progress(self, counter=0):
        if self.event_ct < self.event_total:
            meta = {'current': self.event_ct, 'total': self.event_total}
            self.update_state(state='PROGRESS', meta=meta)

            self.event_ct += 10
        return self.event_ct


    def get__namespace(self, instance):
        """
        get namespace
        """
        return instance.get('kind')

    def get__model_obj(self):
        """
        return model from the instance
        or 
        my_model = type(my_instance)
        """

        # obj = model_name
        app_label, model_name = self.model.split(".")
        # app_name = app_label
        obj = apps.get_model(app_label=app_label, model_name=model_name)

        # i = Invoice.objects.filter(id=1234).first()
        # return obj.objects.all()

        # obj = AppConfig.get_models(self.model)

        return obj #instance._meta.model


    def get__model(self, name):

        app_label = "core"

        if "." in name:
            app_label, name = name.split(".")

        obj = apps.get_model(app_label=app_label, model_name=name)

        return obj, name


    # def get_ansible_version(self, instance):
    #     if not hasattr(self, '_ansible_version'):
    #         self._ansible_version = _get_ansible_version(
    #             ansible_path=self.get_path_to_ansible(instance, executable='ansible'))
    #     return self._ansible_version


    # def get__path_to(self, *args):
    #     '''
    #     Return absolute path relative to this file.
    #     '''
    #     return os.path.abspath(os.path.join(os.path.dirname(__file__), *args))


    # def get__path_to_ansible(self, instance, executable='ansible-playbook', **kwargs):

    #     venv_path = getattr(instance, 'ansible_virtualenv_path', settings.ANSIBLE_VENV_PATH)
    #     venv_exe = os.path.join(venv_path, 'bin', executable)
    #     if os.path.exists(venv_exe):
    #         return venv_exe
    #     return shutil.which(executable)


    def build__params_process_isolation(self, instance, private_data_dir, cwd):
        '''
        Build ansible runner .run() parameters for process isolation.
        '''
        process_isolation_params = dict()

    #     if self.should_use_proot(instance):
    #         local_paths = [private_data_dir]
    #         if cwd != private_data_dir and Path(private_data_dir) not in Path(cwd).parents:
    #             local_paths.append(cwd)
    #         show_paths = self.proot_show_paths + local_paths + \
    #             settings.AWX_PROOT_SHOW_PATHS

    #         # Help the user out by including the collections path inside the bubblewrap environment
    #         if getattr(settings, 'AWX_ANSIBLE_COLLECTIONS_PATHS', []):
    #             show_paths.extend(settings.AWX_ANSIBLE_COLLECTIONS_PATHS)

        # pi_path = settings.AWX_PROOT_BASE_PATH

        # path = tempfile.mkdtemp(prefix='awx_%s_' % instance.pk, dir=settings.AWX_PROOT_BASE_PATH)
        # os.chmod(path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)


        pi_path = tempfile.mkdtemp(
            prefix='ansible_runner_pi_',
            dir=settings.AHOME_PROOT_BASE_PATH
        )

        os.chmod(pi_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
        self.cleanup_paths.append(pi_path)

        process_isolation_params = {
            'process_isolation': True,
            'process_isolation_path': pi_path,
            'process_isolation_hide_paths': [
                settings.AHOME_PROOT_BASE_PATH,
            ],
            # 'process_isolation_show_paths': show_paths,
            # 'process_isolation_hide_paths': [
            #     settings.AWX_PROOT_BASE_PATH,
            #     '/etc/tower',
            #     '/etc/ssh',
            #     '/var/lib/awx',
            #     '/var/log',
            #     settings.PROJECTS_ROOT,
            #     settings.JOBOUTPUT_ROOT,
            # ] + getattr(settings, 'AWX_PROOT_HIDE_PATHS', None) or [],
            # 'process_isolation_ro_paths': [settings.ANSIBLE_VENV_PATH, settings.AWX_VENV_PATH],
        }

        logger.info("process_isolation_params : \n{}".format(process_isolation_params))




        return process_isolation_params



    def build__private_data_dir(self, instance):
        """
        .
        ├── env
        │   ├── envvars
        │   ├── extravars
        │   ├── passwords
        │   ├── cmdline
        │   ├── settings
        │   └── ssh_key
        ├── inventory
        │   └── hosts
        ├── project
        │   └── test.yml
        └── roles
            └── testrole
                ├── defaults
                ├── handlers
                ├── meta
                ├── README.md
                ├── tasks
                ├── tests
                └── vars

        """
        try:

            if not os.path.exists(settings.AHOME_PROOT_BASE_PATH):
                os.mkdir(settings.AHOME_PROOT_BASE_PATH)
            os.chmod(settings.AHOME_PROOT_BASE_PATH, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
            

            uuid = instance.get('uuid')

            path = tempfile.mkdtemp(prefix='ahome_%s_' % uuid, dir=settings.AHOME_PROOT_BASE_PATH)

            if not os.path.exists(path):
                os.mkdir(path)
            
            os.chmod(path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)


            logger.info("tmp path dir:  {}".format(path))
            
            for folder in ['env', 'inventory', 'project', 'roles']:

                directory = os.path.join(path, folder)

                if not os.path.exists(directory):
                    os.mkdir(directory)
            
                os.chmod(directory, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)


            return path
            
        except Exception as e:
            raise e

    def get__parent_credentials(self, instance):

        parent = dict()
        inherit_credentials = instance.get('credentials') or {}
        
        for parent_model, parent_pk in inherit_credentials.items():
            obj_parent = apps.get_model(app_label='core', model_name=parent_model)
            dataset = obj_parent.objects.filter(pk=parent_pk).values()
            for data in dataset:
                parent['cloud'] = data.get('cloud', False)
                parent['inputs'] = data.get('inputs', dict())

        return parent

    def get__instance_inputs(self, instance, model_name):

        instance_inputs = dict(
            cloud = False,
            inputs = dict()
            )
        try:
            if "." in model_name:
                app_label, model_name = model_name.split(".")

            obj, objname = self.get__model(model_name)
            pk = instance.get(model_name)
            dataset = obj.objects.filter(pk=pk).values('cloud', 'inputs')
            # logger.info("get__instance_inputs: {} => {} -- {}".format(model_name, pk, dataset))
            for data in dataset:
                instance_inputs['cloud']  = data.get('cloud', False)
                instance_inputs['inputs'] = data.get('inputs', dict())
        except Exception as e:
            # raise e
            logger.info("get__instance_inputs error:  {}".format(e))

        return instance_inputs


    def build__envvars(self, instance, private_data_dir, **kwargs):
        kind = instance.get('kind')
        cloud = instance.get('cloud')
        inputs = instance.get('inputs')

        ## build parent envvars

        ## Build virtual env
        env = dict(os.environ.items())
        venv_path = settings.ANSIBLE_VENV_PATH
        env['VIRTUAL_ENV'] = venv_path
        env['PATH'] = os.path.join(venv_path, "bin") + ":" + env['PATH']

        # obj = apps.get_model(app_label=app_label, model_name=model_name)
        parent = self.get__parent_credentials(instance)
        ##


        if cloud or parent.get('cloud'):

            if parent.get('inputs'):
                inputs = parent['inputs']


        inputs = {k.upper():v for k,v in inputs.items()} if inputs else {}

        inputs.update(dict(
            DEFAULT_GATHERING = 'implicit', #'explicit',
            ANSIBLE_GATHERING = 'implicit', #'explicit',
            VIRTUAL_ENV = venv_path,
            PATH = env['PATH'],
            # ANSIBLE_STDOUT_CALLBACK = 'json',
            ANSIBLE_STDOUT_CALLBACK = 'counter_enabled',
            # ANSIBLE_STDOUT_CALLBACK
            DEFAULT_STDOUT_CALLBACK = 'counter_enabled',
            # MS AZURE
            REQUESTS_CA_BUNDLE = f"{venv_path}/lib/python3.6/site-packages/certifi/cacert.pem",

            AHOME_ID = instance.get('uuid'),
            AHOME_MODEL = self.model,
            AHOME_ACTION = instance.get('action'),

            )
        )

        if kwargs.get('action'):
            inputs.update( dict(
                AHOME_ACTION = kwargs.get('action'),
                )
            )

        if kwargs.get('credentials'):
            inputs.update( dict(
                SSH_PUB = kwargs.get('credentials', {}).get('ssh_pub',''),
                )
            )


        # logger.info("envvars inputs {}".format(inputs))


        content = yaml.safe_dump( inputs )

        self.helper__create_yaml(private_data_dir, 'env', 'envvars', content)

        return os.path.join(private_data_dir, "env/envvars")



    def build__extravars(self, instance, private_data_dir, vars):

        kind = instance.get('kind')
        inputs = instance.get('inputs')
        cloud = instance.get('cloud')

        extravars = dict()

        if cloud:

            extravars.update(dict(
                ansible_connection = 'local',
                ansible_python_interpreter = "/venv/ansible/bin/python"
                ))

        content = yaml.safe_dump( extravars )

        self.helper__create_yaml(private_data_dir, 'env', 'extravars', content)
            

        return os.path.join(private_data_dir, "env/extravars")
        
        
    def helper__create_yaml(self, private_data_dir, directory, file, content, header = None):
        
        path = os.path.join(private_data_dir, directory)

        # logger.info("{} path:  {}".format(directory, path))
        
        try:
            os.mkdir(path, stat.S_IREAD | stat.S_IWRITE | stat.S_IEXEC)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        path = os.path.join(path, file)


        handle = os.open(path, os.O_RDWR | os.O_CREAT, stat.S_IREAD | stat.S_IWRITE)

        f = os.fdopen(handle, 'w')

        f.write(content)

        f.close()

        os.chmod(path, stat.S_IRUSR)

        return path

    def build__secrets(self, instance, private_data_dir):
        pass

    def build__sshkey(self, instance, private_data_dir):
        '''
        Creates temporary files containing the private data.
        Returns a dictionary i.e.,
        {
            'sshkeys': {
                'privatekey': '/path/to/decrypted/private_data',
                'publickey': '/path/to/decrypted/public_data',
                ...
            }
        }
        '''

        kind = instance.get('kind')
        inputs = instance.get('inputs', {})
        cloud = instance.get('cloud')

        # logger.info("iaas:  {}".format(instance.get('iaas')))

        sshkey_files = dict( credentials = dict() )

        sshkey = dict (
            privatekey = inputs.get('privatekey', None),
            publickey  = inputs.get('publickey', None)
            )

        if sshkey.get('privatekey') is None:
            iaas_instance = self.get__instance_inputs(instance, 'core.iaas')
            iaas_inputs = iaas_instance.get('inputs', {})
            
            # logger.info("iaas inputs:  {}".format(iaas_inputs))
            
            sshkey = dict (
                privatekey = iaas_inputs.get('privatekey', None),
                publickey  = iaas_inputs.get('publickey', None)
                )


        if  not sshkey.get('privatekey') is None:
            ssh_ver = get_ssh_version()
            ssh_too_old = True if ssh_ver == "unknown" else Version(ssh_ver) < Version("6.0")
            openssh_keys_supported = ssh_ver != "unknown" and Version(ssh_ver) >= Version("6.5")

            data = sshkey.get('privatekey')
            
            # Bail out now if a private key was provided in OpenSSH format
            # and we're running an earlier version (<6.5).
            if 'OPENSSH PRIVATE KEY' in data and not openssh_keys_supported:
                raise RuntimeError(OPENSSH_KEY_ERROR)
            # OpenSSH formatted keys must have a trailing newline to be
            # accepted by ssh-add.
            if 'OPENSSH PRIVATE KEY' in data and not data.endswith('\n'):
                data += '\n'
            # For credentials used with ssh-add, write to a named pipe which
            # will be read then closed, instead of leaving the SSH key on disk.
            
            if not cloud and not ssh_too_old:
                try:
                    os.mkdir(os.path.join(private_data_dir, 'env'))
                except OSError as e:
                    if e.errno != errno.EEXIST:
                        raise
                path = os.path.join(private_data_dir, 'env', 'ssh_key')
                # ansible_runner.utils.open_fifo_write(path, data.encode())
                sshkey_files['credentials']['ssh'] = path

            # Ansible network modules do not yet support ssh-agent.
            # Instead, ssh private key file is explicitly passed via an
            # env variable.
            else:
                handle, path = tempfile.mkstemp(dir=private_data_dir)
                f = os.fdopen(handle, 'w')
                f.write(data)
                f.close()
                os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
            sshkey_files['credentials']['ssh_key'] = path
            sshkey_files['credentials']['ssh_pub'] = sshkey.get('publickey')

            # -- 

            handle, path = tempfile.mkstemp(dir=private_data_dir)
            f = os.fdopen(handle, 'w')
            f.write(data)
            f.close()
            os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)

            sshkey_files['credentials']['ssh_priv'] = path

            # logger.info("ssh key write path:  {}".format(path))

            # --

            # parent = self.get__parent_credentials(instance)

        return sshkey_files
    
    def build__private_data_files(self, instance, private_data_dir):
        '''
        Creates temporary files containing the private data.
        Returns a dictionary i.e.,
        {
            'credentials': {
                <awx.main.models.Credential>: '/path/to/decrypted/data',
                <awx.main.models.Credential>: '/path/to/decrypted/data',
                ...
            },
            'certificates': {
                <awx.main.models.Credential>: /path/to/signed/ssh/certificate,
                <awx.main.models.Credential>: /path/to/signed/ssh/certificate,
                ...
            }
        }
        '''
        private_data = self.build__private_data(instance, private_data_dir)
        
        private_data_files = {'credentials': {}}
        if private_data is not None:
            ssh_ver = get_ssh_version()
            ssh_too_old = True if ssh_ver == "unknown" else Version(ssh_ver) < Version("6.0")
            openssh_keys_supported = ssh_ver != "unknown" and Version(ssh_ver) >= Version("6.5")
            for credential, data in private_data.get('credentials', {}).items():
                # Bail out now if a private key was provided in OpenSSH format
                # and we're running an earlier version (<6.5).
                if 'OPENSSH PRIVATE KEY' in data and not openssh_keys_supported:
                    raise RuntimeError(OPENSSH_KEY_ERROR)
                # OpenSSH formatted keys must have a trailing newline to be
                # accepted by ssh-add.
                if 'OPENSSH PRIVATE KEY' in data and not data.endswith('\n'):
                    data += '\n'
                # For credentials used with ssh-add, write to a named pipe which
                # will be read then closed, instead of leaving the SSH key on disk.
                if credential and credential.credential_type.namespace in ('ssh', 'scm') and not ssh_too_old:
                    try:
                        os.mkdir(os.path.join(private_data_dir, 'env'))
                    except OSError as e:
                        if e.errno != errno.EEXIST:
                            raise
                    path = os.path.join(private_data_dir, 'env', 'ssh_key')
                    ansible_runner.utils.open_fifo_write(path, data.encode())
                    private_data_files['credentials']['ssh'] = path
                # Ansible network modules do not yet support ssh-agent.
                # Instead, ssh private key file is explicitly passed via an
                # env variable.
                else:
                    handle, path = tempfile.mkstemp(dir=private_data_dir)
                    f = os.fdopen(handle, 'w')
                    f.write(data)
                    f.close()
                    os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
                private_data_files['credentials'][credential] = path
            
            for credential, data in private_data.get('certificates', {}).items():
                artifact_dir = os.path.join(private_data_dir, 'artifacts', str(self.instance.id))
                if not os.path.exists(artifact_dir):
                    os.makedirs(artifact_dir, mode=0o700)
                path = os.path.join(artifact_dir, 'ssh_key_data-cert.pub')
                with open(path, 'w') as f:
                    f.write(data)
                    f.close()
                os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
        return private_data_files


# TODO: Move credential to proper secured model

    # def build__private_data(self, instance, private_data_dir):
    #     '''
    #     Returns a dict of the form
    #     {
    #         'credentials': {
    #             <awx.main.models.Credential>: <credential_decrypted_ssh_key_data>,
    #             <awx.main.models.Credential>: <credential_decrypted_ssh_key_data>,
    #             ...
    #         },
    #         'certificates': {
    #             <awx.main.models.Credential>: <signed SSH certificate data>,
    #             <awx.main.models.Credential>: <signed SSH certificate data>,
    #             ...
    #         }
    #     }
    #     '''
    #     private_data = {'credentials': {}}
    #     for credential in job.credentials.prefetch_related('input_sources__source_credential').all():
    #         # If we were sent SSH credentials, decrypt them and send them
    #         # back (they will be written to a temporary file).
    #         if credential.has_input('ssh_key_data'):
    #             private_data['credentials'][credential] = credential.get_input('ssh_key_data', default='')
    #         if credential.has_input('ssh_public_key_data'):
    #             private_data.setdefault('certificates', {})[credential] = credential.get_input('ssh_public_key_data', default='')

    #     return private_data







    def build__inventory(self, instance, private_data_dir, **kwargs):


        hosts = dict(
            all = dict (
                hosts = dict(
                ),
                vars = dict(),
                children = dict(),
            )
        )
        DEFAULT_DUMMY_INPUTS = {
            "inventory": "localhost",
            "username": "root"
        }

        inputs = instance.get('inputs') or DEFAULT_DUMMY_INPUTS
        cloud  = instance.get('cloud')

        parent = self.get__parent_credentials(instance)

        inventory = dict()

        if cloud or parent.get('cloud'):
            inventory = dict(
                ansible_host = "localhost",
                )
        elif parent.get("inputs"):
            pinputs = parent.get("inputs")
            inventory = dict(
                ansible_host = pinputs.get("inventory", "localhost"),
                ansible_user = pinputs.get("username", "root"),
                )
        else:
            inventory = dict(
                ansible_host = inputs.get("inventory", "localhost"),
                ansible_user = inputs.get("username", "root"),
                )

        inventory.update(dict(
            ansible_ssh_private_key_file=kwargs.get('credentials', {}).get('ssh_priv',''),
            )
        )



        custom_slugify = Slugify(to_lower=True)
        custom_slugify.separator = '_'
        inventory_name = custom_slugify(instance.get('name'))

        hosts['all']['hosts'][inventory_name] = inventory

        # send ahome parameters as variables
        # a
        #
        inputs.update( dict(
            ahome__id = instance.get('uuid'),
            ahome__model = self.model,
            ahome__action = instance.get('action'),
            )
        )

        if kwargs.get('action'):
            inputs.update( dict(
                ahome__action = kwargs.get('action'),
                )
            )

        # remove ssh private key in vars
        inputs.pop('privatekey', None)


        hosts['all']['vars'] = inputs


        content = yaml.dump(hosts, default_flow_style=False)

        # logger.info("hosts:  {}".format(content))

        return self.helper__create_yaml(private_data_dir, 'inventory', 'hosts', content)


    def build__roles(self, instance, private_data_dir, namespace):
        roles_path_base = '{}/{}'.format(settings.AHOME_LOCAL_ANSIBLE_ROLES_PATH, namespace)
        roles_path = os.path.join(private_data_dir, 'roles/{}'.format(namespace))

        logger.info("Building roles for namespace: '{}'; source: '{}' target: '{}' ...".format(
            namespace, roles_path_base, roles_path))

        try:
            copy_tree(roles_path_base, roles_path)
        except:
            logger.critical("Cannot build roles "
                            "for namespace: '{}'; "
                            "source: '{}' "
                            "target: '{}' ...".format(namespace, roles_path_base, roles_path))
            raise

        return os.path.join(private_data_dir, 'roles')

    def save__job(self):

        ident = self.instance.get('uuid')

        obj = self.get__model_obj()

        e = obj.objects.get(uuid=ident)
        e.status = self.job_defaults.get("status")
        e.action = self.action
        e.runner = self.job_defaults
        e.save()
  
        # obj, _created = Job.objects.update_or_create(
        #     ident = ident, name = "{}/{}".format(self.namespace, ident),
        #     defaults = self.job_defaults,
        # )


        return obj


    def event_handler(self, event_data):


        # logger.info("** runner {}".format(event_data) )

        # progress bar purpose only
        progress = self.job_defaults.get("celery_progress") + randrange(10)
        if progress <= 90 :
            self.job_defaults.update( dict(
                            celery_progress = progress ,
                        )
                    )
            save_job = self.save__job()

        
        # event dispatch
        self.event_ct +=1
        self.workflow__job_event(self.instance, event_data, self.namespace)




        if event_data.get('event') == 'playbook_on_stats':
            stats = dict()
            e = event_data.get('event_data')
            for key in [ 'changed', 'dark', 'failures', 'ignored', 'ok', 'processed', 'rescued', 'skipped', 'created' ]:
                stats.update( { key : e.get(key, dict())} )

            self.job_defaults.update( dict(
                        stats = stats,
                    )
                )

        if event_data.get('event') == 'runner_on_failed':

            e = event_data.get('event_data')

            fail_msg = e.get('res').get('msg')

            self.job_defaults.update( dict(
                        fail_msg = fail_msg,
                    )
                )

            self.notifications.update( dict(
                alert = 'danger',
                verb = 'failed',
                msg = fail_msg,

                ) )




        # self.event_ct +=1
        # logger.info("** runner {} {} {}".format(self.task_id, self.event_ct, self.event_total))

    def finished_callback(self, runner_obj):

        # pass
        self.job_defaults.update( dict(
                    status = runner_obj.status,
                    rc = runner_obj.rc,
                    celery_progress = 100,
                    celery_event_ct = self.event_ct
                )
            )

        save_job = self.save__job()


        self.notifications.update( dict(
                alert = runner_obj.status,
                verb = runner_obj.status,

                ) )

        self.emit__channel_notification()

        # event_data = {
        #             'event': 'EOF',
        #             'final_counter': self.event_ct,
        #         }

        # logger.info("** final callback last_stdout_update: {} status: {} errored: {} **".format( runner_obj.last_stdout_update, runner_obj.status, runner_obj.errored ))
        # logger.info("** final callback events: {} status: {} stats: {} **".format( runner_obj.events, runner_obj.status, dir(runner_obj.events) ))


    def status_handler(self, status_data, runner_config):

        self.job_defaults.update( dict(
                    status = status_data['status'],
                )
            )

        save_job = self.save__job()



        # logger.info("** status handler {} **".format(status_data['status']))
        # job_env = dict(runner_config.env)
        # logger.info("** status handler job_env {} ** args: {}".format(job_env,json.dumps(runner_config.command) ))

        '''
        Ansible runner callback triggered on status transition
        '''
        # if status_data['status'] == 'starting':
        #     job_env = dict(runner_config.env)
        #     '''
        #     Take the safe environment variables and overwrite
        #     '''
        #     for k, v in self.safe_env.items():
        #         if k in job_env:
        #             job_env[k] = v
        #     self.instance = self.update_model(self.instance.pk, job_args=json.dumps(runner_config.command),
        #                                       job_cwd=runner_config.cwd, job_env=job_env)




    # def event__dispatch(self, instance, namespace, runner):


    #     # for each_host_event in runner.events:
    #     # event_ct = 0

    #     for i, each_host_event in enumerate(runner.events):

    #         #progress bar
    #         # self.set__progress()
    #         self.event_ct +=1
    #         # logger.info("** runner {} {} {}".format(self.task_id, self.event_ct, self.event_total))
    #         self.workflow__job_event(instance, each_host_event, namespace)


    def workflow__job_event(self, instance, job_event, namespace):

        event = job_event.get('event')
        event_data = job_event.get('event_data')
        ident = job_event.get('runner_ident')

        if event == 'runner_on_ok':

            facts = self.save__ansible_facts(instance, event_data, namespace)

            # self.save__ipaddresses(instance, facts, namespace)

            if namespace == 'Setup':
                pass
#TODO - FIX generic
            elif namespace == 'generic':
                self.workflow__job_ec2(instance, job_event, namespace)
            else:
                self.workflow__job(instance, job_event, namespace)

            # if namespace == 'kvm':
            #     # KVM
            #     # self.workflow__job_kvm(instance, job_event, namespace)
            #     self.workflow__job_ec2(instance, job_event, namespace)

            # if namespace == 'ec2':
            #     # EC2
            #     self.workflow__job_ec2(instance, job_event, namespace)

            # if namespace == 'generic':
            #     # EC2
            #     self.workflow__job_ec2(instance, job_event, namespace)

            # if namespace == 'amazon_ec2':
            #     # EC2
            #     self.workflow__job(instance, job_event, namespace)


        return


    def workflow__job(self, instance, job_event, namespace):

        event = job_event.get('event')
        event_data = job_event.get('event_data')
        ident = job_event.get('runner_ident')

        # logger.info(event_data)

        if event_data.get('task_action') == 'debug' :

            e_data = event_data.get("res", dict)

            ahomefile_data = ahomefile_to_dict(namespace)

            # logger.info( instance )

            uniqueKeys = []
            
            for k in e_data.keys():
                query = "$.ansibleObjects.where($.metadata.anchor = '{}' and $.kind ='ModelInjector')".format(k)
                query_output = dict_yaql(ahomefile_data, query)
                
                # logger.info(f"Query: {query}")
                
                if len(query_output) > 0:
                    # logger.info( "{} ** {}".format(k, query_output) )
                    for query_data in query_output:
                        
                        query = "$.{}".format( query_data.get('metadata').get('entrypoint') )
                        query_entries = dict_yaql(e_data, query)
                        try:
                            if len(query_entries) > 0:
                                for entry_data in query_entries:

                                    data = self.workflow__construct_fields(query_data, ahomefile_data, e_data, entry_data)

                                    if data:
                                        self.workflow__job_save(instance, query_data, data)
                                        uniqueKeys.append( data.get('unique_keys'))

                        except Exception as e:
                            # raise e
                            logger.warning( f"core/tasks/base_tasks.py: Error {e} =>  {query}" )

            # clean
                query = "$.ansibleObjects.where($.metadata.anchor = '{}' and $.kind ='ModelCleaner')".format(k)
                # logger.info(query)
                query_output = dict_yaql(ahomefile_data, query)
                if len(query_output) > 0:
                    # logger.info( "{} ** {}".format(k, query_output) )
                    for query_data in query_output:
                        self.workflow__job_clean_orphans(instance, query_data, uniqueKeys)

            


        return True



    def workflow__job_clean_orphans(self, instance, query_data, unique_keys):

        """
        clean orphan records
        """

        obj, objname = self.get__model(query_data.get('metadata').get('model'))

        selfobj, selfobjname = self.get__model(self.model)

        if selfobjname in [f.name for f in obj._meta.get_fields(include_hidden=True)]:

            filters = { '{}__uuid__exact'.format(selfobjname): '{}'.format(instance.get("uuid")) }

            # logger.info( "{} -- {}".format("objfields", [f.name for f in obj._meta.get_fields(include_hidden=True)]) )

            queryset = obj.objects.filter( **filters ).values("id", "name", "unique_keys")

            # logger.info( "{} ** {}".format("Clean", queryset) )

            # logger.info( "{} -- {}".format("Clean ** uniqueKeys", unique_keys) )

            for qs in queryset:
                remove = qs.get('id')
                for unique_key in unique_keys:
                    # logger.info( "compare: {} -- {}".format(qs.get('unique_keys'), unique_key) )
                    if qs.get('unique_keys') == unique_key:
                        remove = 0
                        # logger.info( "!!! matched: {} -- {}".format(qs.get('unique_keys'), unique_key) )
                        continue
                if remove > 0:
                    obj.objects.filter( id = remove ).delete()


       


    def workflow__job_save(self, instance, query_data, data):
        """

        """
        # logger.info( f"core/tasks/base_tasks.py -> workflow__job_save: Saving/Updating instance: {instance}" )

        obj, objname = self.get__model(query_data.get('metadata').get('model'))
        fobj = obj.objects.filter(unique_keys__contains = data.get('unique_keys'))

        if fobj:
            for ds in fobj:
                qobj = obj.objects.get( pk=ds.id )
                for key, value in data.items():
                    setattr(qobj, key, value)
                qobj.save()
                logger.info("save model: {}".format(objname))
        else:

            selfobj, selfobjname = self.get__model(self.model)

            qobj = selfobj.objects.get( uuid=instance.get('uuid') )

            data.update( {selfobjname: qobj} )

            obj.objects.create(**data)
            logger.info("create entry in model: {}".format(objname))


        return True



    def workflow__construct_fields(self, query_data, ahomefile_data, e_data, entry_data):

        # logger.info( "{} ** {}".format("Query Data", query_data) )


        obj, objname = self.get__model(query_data.get('metadata').get('model'))
        objfields = [f.name for f in obj._meta.get_fields()]


        # ahomefile_yaql


        # logger.info( "{} -- {}".format("objfields", [f.name for f in obj._meta.get_fields(include_hidden=True)]) )

        # uniqueKeys fields
        uniqueKeys = dict()
        for f in query_data.get('spec').get('uniqueKeys'):
            field = self.workflow__interpolate_atomic_fields(f, ahomefile_data, e_data, entry_data)
            uniqueKeys.update( {field.get('fieldRef'): field.get('value')} )

        # logger.info( "{} -- {}".format("uniqueKeys", uniqueKeys) )

        fields = []
        for f in query_data.get('spec').get('modelFields'):
            field = self.workflow__interpolate_atomic_fields(f, ahomefile_data, e_data, entry_data)

            fields = append_ahomefile_fields(fields, field)

        # logger.info( "{} -- {}".format("fields", fields) )

        sobj = dict()
        setfacts = dict()
        for f in fields:
            _obj = { f.get('fieldRef'): f.get('value') }
            setfacts.update(_obj)
            if f.get('fieldRef') in objfields:
                sobj.update(_obj)

        sobj.update( { 'unique_keys': uniqueKeys } )
        sobj.update( { 'setfacts': setfacts } )

        # logger.info( "{} -- {}".format("final fields", sobj) )

        return sobj



    def workflow__interpolate_atomic_fields(self, q_field, ahomefile_data, e_data, entry_data):

        """
        - name: instance_id
          value: xxxxx.          # set value or yaqlRef or valueRef -- not all. value overrides all refs
          fieldRef: instance_id
          yaqlRef: $.consumers.....
          valueRef: xxxxx
        """
        a_field = dict()
        a_field['name'] = q_field.get("name")
        a_field['fieldRef'] = q_field.get("fieldRef", q_field.get("name") )



        if q_field.get("value"):
            a_field['value'] = q_field.get("value")
            return a_field

        if q_field.get("valueRef"):
            """
            TODO
            wizardObjects:
              metadata:
                name: wizardbox
                model: core.iaas 
            """
            a_field['value'] = q_field.get("value")

            return a_field

        if q_field.get("yaqlRef"):
            """
            """
            query = q_field.get("yaqlRef")
            a_field['value'] = ahomefile_yaql(entry_data, query)

            # logger.info( "{} -- {}".format("yaqlRef", a_field) )

            
            return a_field


        return dict()



    def workflow__job_ec2(self, instance, job_event, namespace):

        event = job_event.get('event')
        event_data = job_event.get('event_data')
        ident = job_event.get('runner_ident')

        # logger.info(event_data)

        if event_data.get('task_action') == 'debug' :

            e__data = event_data.get("res", dict)

            map__output = dict() #OrderedDict()
            ahomefile = "{}/{}.yml".format(settings.AHOMEMAPPINGS_PATH, namespace)

            map__data = load_yml_to_dict(ahomefile)
            


            map__output["name"] = map__data.get("name")
            map__output["description"] = map__data.get("description")
            map__output["title"] = map__data.get("title")
            map__output["cloud"] = map__data.get("cloud", False)
            map__output["version"] = map__data.get("version", '1.0')

            map__output["facts"] = []
            # map__output["expose"] = []
            # map__key = dict()

            key__output = []

            registered__vars = map__data.get("registered_vars", dict())


            

            for r__var in e__data.keys():

                if registered__vars.get(r__var):

                    r__key = registered__vars[r__var].get("name", r__var)
                    r__model = registered__vars[r__var].get("model")
                    r__adhoc = registered__vars[r__var].get("adhoc", False)
                    r__entrypoint = registered__vars[r__var].get("entrypoint")
                    r__links = registered__vars[r__var].get("expose", dict())
                    r__unique_keys = registered__vars[r__var].get("unique_keys", dict())
                    r__defaults = registered__vars[r__var].get("defaults", dict())
                    r__inputs = registered__vars[r__var].get("inputs", dict())


                    ## SKIP if there is not ahome__id and ahome__model defined

                    # SET ITEMS TO BE DELETED
                    if e__data[r__var].get("ahome__id") and e__data[r__var].get("ahome__model") and r__model :

                        # logger.info( e__data[r__var].get("ahome__id") )
                        # logger.info( e__data[r__var].get("ahome__model") )
                        # logger.info( r__model )

                        data__delete = dict(
                            ahome__id = e__data[r__var].get("ahome__id"),
                            ahome__model = e__data[r__var].get("ahome__model"),
                            model = r__model,

                            )
                        self.workflow__delete(instance, data__delete, delete=False)


                    
                    if not e__data[r__var].get("ahome__id") or not e__data[r__var].get("ahome__model") :
                        continue

                    if e__data[r__var].get(r__entrypoint):

                        ## TODO: remove Debug
                        # logger.info(e__data)

                        d__entries = e__data[r__var][r__entrypoint]

                        # logger.info(d__entries)

                        for d__entry in d__entries:


                            map__key = dict(
                                ahome__id = e__data[r__var].get("ahome__id"),
                                ahome__model = e__data[r__var].get("ahome__model"),
                                name = r__key,
                                model = r__model,
                                adhoc = r__adhoc,
                                unique_keys = dict(),
                                fields = dict(),
                                expose = dict(),
                                defaults = dict(),
                                inputs = dict(),
                            )

                            r__fields = dict()
                            r__expose = dict()

                            logger.info("init {} map__key: {}".format(d__entry, map__key))


                            for r__link in r__links:
                                r__name = r__link.get("name")
                                r__type = r__link.get("type")
                                r__save = r__link.get("save",False)

                                ## -- TODO type to check after... not before.
                                r__reference = None
                                r__refs = r__link.get("ref",r__name).split(".")

                                # r__reference = d__entry.get(r__refs[0])

                                x__max = len(r__refs) -1
                                x = 0
                                while x <= x__max:
                                    # logger.info("x : {} r__refs[x]: {} r__reference: {}".format(x, r__refs[x], r__reference ))
                                    
                                    regexp = re.compile(r"\[(\d+)\]")
                                    f__name = r__refs[x]
                                    index = 0
                                    search = False

                                    try:

                                        if regexp.search(f__name):
                                            index = int(regexp.findall(f__name)[0])
                                            search = True
                                            f__name = f__name.replace("[{}]".format(index), "")

                                        if x == 0:
                                            
                                            if search:
                                                r__reference = d__entry.get(f__name)[index]
                                            else:
                                                r__reference = d__entry.get(f__name)

                                        else:

                                            if search:
                                                r__reference = r__reference.get(f__name)[index]
                                            else:
                                                r__reference = r__reference.get(f__name)


                                    except Exception as e:
                                        # raise e
                                        pass
                                        ## TODO: Based on reference type output the reference default type

                                    x = x + 1

                                # map__output["expose"].append( { r__name: r__reference } )
                                # map__key["expose"].append( { r__name: r__reference } )
                                r__expose.update( { r__name: r__reference } )
                                if r__save:
                                    # map__output["fields"].append( { r__name: r__reference } )
                                    # map__key["fields"].append( { r__name: r__reference } )
                                    r__fields.update( { r__name: r__reference } )


                            map__key["fields"] =  r__fields
                            map__key["expose"] = r__expose


                            # unique keys
                            key__dict = dict()

                            for r__unique_key in r__unique_keys:
                                if r__expose.get(r__unique_key):
                                    key__dict.update( { r__unique_key: r__expose.get(r__unique_key) } )

                            map__key["unique_keys"] = key__dict


                            # defaults
                            defaults__dict = dict(
                                is_obselete = False,
                                )

                            for r__default in r__defaults:
                                k = r__default.get("name")
                                v = r__default.get("value")
                                s = r__default.get("static", None)


                                if s:
                                    defaults__dict.update( { k: v } )
                                else:                            
                                    if r__expose.get(v):
                                        defaults__dict.update( { k: r__expose.get(v) } )

                            map__key["defaults"] = defaults__dict


                            # inputs
                            inputs__dict = dict()

                            for r__input in r__inputs:
                                k = r__input.get("name")
                                v = r__input.get("value")
                                s = r__input.get("static", None)

                                if s:
                                    inputs__dict.update( { k: v } )
                                else:                            
                                    if r__expose.get(v):
                                        inputs__dict.update( { k: r__expose.get(v) } )

                            map__key["inputs"] = inputs__dict




                            # final output map__output
                            logger.info("map__key: {}".format(map__key))

                            if r__adhoc:
                                self.workflow__adhoc_save(instance, map__key)
                            else:
                                self.workflow__save(instance, map__key)




                            # key__output.append(map__key)

                            # map__output["facts"].append( map__key )




                    # DELETE ORPHANS
                    if e__data[r__var].get("ahome__id") and e__data[r__var].get("ahome__model") and r__model :

                        data__delete = dict(
                            ahome__id = e__data[r__var].get("ahome__id"),
                            ahome__model = e__data[r__var].get("ahome__model"),
                            model = r__model,
                            )

                        self.workflow__delete(instance, data__delete, delete=True)



            # logger.info("map__output: {}".format(map__output))

            # logger.info("key__output: {}".format(key__output))

            # self.workflow__save(instance, map__output)


        return True

    def workflow__delete(self, instance, data, delete=False ):
        """
        mark records for delation / set is_obslete to true
        """
        # TODO: convert iaas into variable
        iaas__model = data.get("ahome__model")
        iaas__uuid = data.get("ahome__id")
        fact__model = data.get("model")

        fact__obj, fact__objname = self.get__model(fact__model)

        if delete:
            fact__obj.objects.filter( is_obselete = True ).delete()
        else:
            fact__obj.objects.filter( iaas__uuid__exact = iaas__uuid ).update(is_obselete = True)






    def workflow__save(self, instance, data):
        """
        OrderedDict(
        [('name', 'amazon ec2'), ('description', 'Amazon Web service EC2 mapping\n'), ('title', 'amazon EC2 mapping file'), ('cloud', True), ('version', 1.0), 
            ('facts', 
                [{'ahome__id': '09765304-c903-4bc5-830d-dc3ef2ba82a8', 
                'ahome__model': ' core.iaas', 'name': 'ec2_facts', 
                'model': 'core.virtualmachines', 
                'fields': 
                    [{'status': 'running', 'primary_ip': '3.122.195.230'}], 
                    'expose': 
                        [{'status': 'running', 'primary_ip': '3.122.195.230', 'block_device_mappings': '/dev/sda1', 
                        'network_interfaces': 'ec2-3-122-195-230.eu-central-1.compute.amazonaws.com', 
                        'group_id': 'sg-f6ba2095', 'architecture': 'x86_64', 'hypervisor': 'xen', 
                        'image_id': 'ami-0badcc5b522737046', 'instance_id': 'i-041ee5352c2d04b0e'}]
                    }]
            )]
        )
        """


        foreign__model = data.get("ahome__model")
        foreign__uuid = data.get("ahome__id")
        fact__model = data.get("model")


        fkobj, fkname = self.get__model(foreign__model)

        foreign__obj = fkobj.objects.get( uuid = foreign__uuid )

        fact__obj, fact__objname = self.get__model(fact__model)

        fact__defaults = self.helper__merge_dicts(data.get("fields"), data.get("defaults") ) # { **fact.get("fields"), **fact.get("defaults") }
        fact__unique_keys = data.get("unique_keys")

        fact_facts = { data.get("name"): data.get("expose") }

        fact_inputs = data.get("inputs")


        logger.info(fact__defaults)
        # logger.info(fact__unique_keys)

        obj = fact__obj.objects.filter(unique_keys__contains = fact__unique_keys)

        logger.info("fact__unique_keys {}".format(fact__unique_keys))

        if obj:
            # update
            logger.info("update {}".format(obj))
            for qs in obj:
                logger.info("updating id: {}".format(qs.id))

                qs_facts = self.helper__merge_dicts(qs.setfacts, fact_facts )

                fact__defaults.update( { 'setfacts': qs_facts } )
                if fact_inputs:
                    fact__defaults.update( { 'inputs': fact_inputs  } )

                # logger.info("updating id: {} with defaults {}".format(qs.id, fact__defaults))

                obj = fact__obj.objects.get( pk=qs.id )
                for key, value in fact__defaults.items():
                    setattr(obj, key, value)
                obj.save()
        else:
            # create
            logger.info("create: {}".format(fact__unique_keys))
            fact__defaults.update( { 'setfacts': fact_facts } )
            if fact_inputs:
                fact__defaults.update( { 'inputs': fact_inputs } )
            new_values = { fkname: foreign__obj, "unique_keys": fact__unique_keys }
            new_values.update(fact__defaults)

            fact__obj.objects.create(**new_values)

            # obj = fact__obj(**new_values)
            # obj.save()



            # try:
            #     obj = fact__obj.objects.get( **{key: val for key, val in fact__unique_keys.items()} )
            #     obj = fact__obj.objects.get( **{key: val for key, val in fact__unique_keys.items()} )
            #     Dog.objects.filter(data__contains={'owner': 'Bob'})
            #     for key, value in fact__defaults.items():
            #         setattr(obj, key, value)
            #     obj.save()
            # except fact__obj.DoesNotExist:
            # # TODO: iaas static to change
            #     new_values = { fact__objname: foreign__obj }
            #     new_values.update(fact__defaults)
            #     obj = fact__obj(**new_values)
            #     obj.save()

        return




    def workflow__adhoc_save(self, instance, data):
        """
        OrderedDict(
        [('name', 'amazon ec2'), ('description', 'Amazon Web service EC2 mapping\n'), ('title', 'amazon EC2 mapping file'), ('cloud', True), ('version', 1.0), 
            ('facts', 
                [{'ahome__id': '09765304-c903-4bc5-830d-dc3ef2ba82a8', 
                'ahome__model': ' core.iaas', 'name': 'ec2_facts', 
                'model': 'core.virtualmachines', 
                'fields': 
                    [{'status': 'running', 'primary_ip': '3.122.195.230'}], 
                    'expose': 
                        [{'status': 'running', 'primary_ip': '3.122.195.230', 'block_device_mappings': '/dev/sda1', 
                        'network_interfaces': 'ec2-3-122-195-230.eu-central-1.compute.amazonaws.com', 
                        'group_id': 'sg-f6ba2095', 'architecture': 'x86_64', 'hypervisor': 'xen', 
                        'image_id': 'ami-0badcc5b522737046', 'instance_id': 'i-041ee5352c2d04b0e'}]
                    }]
            )]
        )
        """


        
        fact__uuid = data.get("ahome__id")
        fact__model = data.get("ahome__model")


        fact__obj, fact__objname = self.get__model(fact__model)

        fact__defaults = self.helper__merge_dicts(data.get("fields"), data.get("defaults") ) # { **fact.get("fields"), **fact.get("defaults") }

        fact_facts = { data.get("name"): data.get("expose") }

        fact__defaults.update( { 'setfacts': fact_facts } )

        if instance.get("setfacts"):
            qs_facts = self.helper__merge_dicts(instance.get("setfacts"), fact_facts )
            fact__defaults.update( { 'setfacts': qs_facts } )

        fact_inputs = data.get("inputs")

        if fact_inputs:
            fact__defaults.update( { 'inputs': fact_inputs  } )



        obj, _created = fact__obj.objects.update_or_create(
            uuid = instance.get('uuid'),
            defaults = fact__defaults,
            )




        return







    def helper__merge_dicts(self, dict1, dict2):
        res = { **dict1, **dict2 }
        return res
                                    



    def workflow__job_kvm(self, instance, job_event, namespace):

        event = job_event.get('event')
        event_data = job_event.get('event_data')
        ident = job_event.get('runner_ident')

        if event_data.get('task_action') == 'debug' :
            
            if event_data.get('res').get('v__virtualmachines'):

                guests_to_register = []

                for vm in event_data['res']['v__virtualmachines']:

                    obj, _ignore = VirtualMachine.objects.update_or_create(
                        name = vm.get('name'), uuid = vm.get('uuid'),  hosted = instance.get('uuid'),
                        defaults = {
                            'definition': vm.get('definition'),
                            'status': vm.get('status'),
                            'kind': 'kvm',
                            'primary_ip': vm.get('interfaces')[0]['ipaddress'],
                            'primary_mac': vm.get('interfaces')[0]['mac'],
                            'interfaces': vm.get('interfaces'),
                            },
                        )

                    guests_to_register.append(dict(
                        name = vm.get('name'),
                        uuid = vm.get('uuid'),
                        status = vm.get('status'),
                        )
                    )

                # save all virtual machines on the hypervisor
                obj, _ignore = Device.objects.update_or_create(
                    uuid = instance.get('uuid'),
                    defaults = {
                            'virtualmachines': guests_to_register,
                            },
                    )

            # SDN

            if event_data.get('res').get('v__sdn'):

                sdn_to_register = []

                for sdn in event_data['res']['v__sdn']:

                    obj, _ignore = Sdn.objects.update_or_create(
                        name = sdn.get('name'), uuid = sdn.get('uuid'),  hosted = instance.get('uuid'),
                        defaults = {
                            'definition': sdn.get('definition'),
                            'status': sdn.get('status'),
                            },
                        )

                    sdn_to_register.append(dict(
                        name = sdn.get('name'),
                        uuid = sdn.get('uuid'),
                        status = sdn.get('status'),
                        )
                    )

                # save all sdn on the hypervisor
                obj, _ignore = Device.objects.update_or_create(
                    uuid = instance.get('uuid'),
                    defaults = {
                            'sdn': sdn_to_register,
                            },
                    )


            # save_sdn_libvirt_kvm(instance, **kwargs)

            # IPAddress
            # save_ip_address_libvirt_kvm(instance, **kwargs)
            if event_data.get('res').get('v__ipaddresses'):

                for ipaddr in event_data['res']['v__ipaddresses']:

                    ip = netaddr.IPNetwork( "{}/{}".format( ipaddr.get('ipaddr'), ipaddr.get('prefix') ) )

                    obj, _ignore = IPAddress.objects.update_or_create(
                        address = ip,  hosted = instance.get('uuid'),
                        defaults = {
                            'definition': ipaddr.get('definition'),
                            'label': "{} ({})".format( ipaddr.get('hostname'), ipaddr.get('mac') ),
                            'status': 5,
                            'description': 'DHCP lease - [imported]',
                            'connected': dict(host=ipaddr.get('hostname'), mac=ipaddr.get('mac') )
                            },
                        )

                    obj, _ignore = Prefix.objects.update_or_create(
                        prefix = netaddr.IPNetwork( "{}/{}".format( ip.network, ipaddr.get('prefix') ) ),
                        defaults = {
                            'status': 5,
                            },
                        )

        return

    def save__ipaddresses(self, instance, facts, namespace):

        if facts.get('ansible_facts'):
            if facts.get('ansible_facts').get('ansible_all_ipv4_addresses'):

                ipaddresses = facts.get('ansible_facts').get('ansible_all_ipv4_addresses')
                # logger.info("ip address:  {}".format(facts))
                for ipv4 in facts.get('ansible_facts').get('ansible_all_ipv4_addresses'):

                    ip = netaddr.IPNetwork( "{}/32".format( ipv4 ) )

                    obj, _ignore = IPAddress.objects.update_or_create(
                        address = ip,  hosted = instance.get('uuid'),
                        defaults = {
                            'definition': instance.get('name'),
                            'label': "{} ({})".format( instance.get('name'), instance.get('primary_mac') ),
                            'status': 1,
                            'description': '{}'.format( instance.get('name') ),
                            'connected': dict(host=instance.get('name'), mac=instance.get('primary_mac') )
                            },
                        )

            if facts.get('ansible_facts').get('ansible_all_ipv6_addresses'):

                for ipv6 in facts.get('ansible_facts').get('ansible_all_ipv6_addresses'):

                    ip = netaddr.IPNetwork( "{}/128".format( ipv6 ) )

                    obj, _ignore = IPAddress.objects.update_or_create(
                        address = ip,  hosted = instance.get('uuid'),
                        defaults = {
                            'definition': instance.get('name'),
                            'label': "{} ({})".format( instance.get('name'), instance.get('primary_mac') ),
                            'status': 1,
                            'description': '{}'.format( instance.get('name') ),
                            'connected': dict(host=instance.get('name'), mac=instance.get('primary_mac') )
                            },
                        )




        return




    def collect__ansible_facts(self, facts):
        
        if not facts.get('ansible_facts'):
            return dict()

        output = dict()
        ansible_facts = copy.deepcopy(facts['ansible_facts'])
        # memory in mb
        output['memory'] = ansible_facts.get('ansible_memory_mb')

        output['fqdn'] = ansible_facts.get('ansible_fqdn')
        output['ipv4'] = ansible_facts.get('ansible_default_ipv4')
        output['ipv6'] = ansible_facts.get('ansible_default_ipv6')
        output['ipaddresses'] = dict(
            ipv4 = ansible_facts.get('ansible_all_ipv4_addresses'),
            ipv6 = ansible_facts.get('ansible_all_ipv6_addresses'),
            )

        # ansible_interfaces
        interfaces = []
        ifaces = ansible_facts.get('ansible_interfaces')
        
        try:
            # remove loopback
            ifaces.remove('lo')

            # if 'lo' in ifaces:
            #     ifaces.remove('lo')

            for iface in ifaces:
                ifname = "ansible_{}".format(iface.replace('-','_'))
                interface = ansible_facts.get(ifname)
                interfaces.append( dict(
                    mtu = interface.get('mtu', None),
                    type = interface.get('type', None),
                    active = interface.get('active', None),
                    device = interface.get('device', None),
                    promisc = interface.get('promisc', None),
                    macaddress = interface.get('macaddress', None),
                    ipv4 = interface.get('ipv4', []),
                    ipv6 = interface.get('ipv6', []),
                    interfaces = interface.get('interfaces', []),
                    )
                )

        except Exception as e:
            pass

        output['interfaces'] = interfaces


        output['processors'] = dict(
            cores = ansible_facts.get('ansible_processor_cores'),
            count = ansible_facts.get('ansible_processor_count'),
            vcpus = ansible_facts.get('ansible_processor_vcpus'),
            threads_per_core = ansible_facts.get('ansible_processor_threads_per_core'),
            processor = ansible_facts.get('ansible_processor'),
            )

        output['mounts'] = ansible_facts.get('ansible_mounts')

        output['os'] = dict(
            system = ansible_facts.get('ansible_system'),
            distribution = ansible_facts.get('ansible_distribution'),
            architecture = ansible_facts.get('ansible_userspace_architecture'),
            release = ansible_facts.get('ansible_distribution_release'),
            version = ansible_facts.get('ansible_distribution_version'),
            )

        output['hardware'] = dict(
            system = ansible_facts.get('ansible_product_name'),
            product_uuid = ansible_facts.get('ansible_product_uuid'),
            product_name = ansible_facts.get('ansible_product_name'),
            product_serial = ansible_facts.get('ansible_product_serial'),
            vendor = ansible_facts.get('ansible_system_vendor'),
            virtualization_type = ansible_facts.get('ansible_virtualization_type'),
            virtualization_role = ansible_facts.get('ansible_virtualization_role'),
            )


        output['lvm'] = ansible_facts.get('ansible_lvm', dict())

        output['lsblk'] = ansible_facts.get('ansible_lsblk', dict())

        if ansible_facts.get('ansible_default_ipv4'):
            output['primary_ip'] = ansible_facts.get('ansible_default_ipv4').get('address', '')
            output['primary_mac'] = ansible_facts.get('ansible_default_ipv4').get('macaddress', '')
        if ansible_facts.get('ansible_default_ipv6'):
            output['primary_ip6'] = ansible_facts.get('ansible_default_ipv6').get('address', '')
            # output['primary_mac'] = ansible_facts.get('ansible_default_ipv6').get('macaddress', '')
        
        
        output['model'] = ansible_facts.get('ansible_product_name')
        # output['kind'] = ansible_facts.get('ansible_virtualization_type')
        output['primary_domain'] = ansible_facts.get('ansible_domain')
        

        return output


    def save__ansible_facts(self, instance, event_data, namespace):

        facts = dict()
        

        if event_data.get('task_action') in ['setup', 'gather_facts'] :

            facts = copy.deepcopy(event_data.get('res'))

            defaults = {
                    'facts': facts,
                    'ident': instance.get('uuid'),
                    'label': instance.get('name'),
                    }

            defaults.update(self.collect__ansible_facts(facts))


            app_label, model_name = self.model.split(".")

            obj = self.get__model_obj()

            if model_name in DEVICE_TEMPLATES:
                _obj, _ignore = obj.objects.update_or_create(
                    uuid = instance.get('uuid'),
                    defaults = defaults,
                    )
            else:
                _obj, _ignore = obj.objects.update_or_create(
                    uuid = instance.get('uuid'),
                    defaults = dict( facts = defaults ),
                    )

            

        return facts


    def emit__notification(self, notif_group, notif_type, notif_message, **kwargs):
        
        channel_layer = get_channel_layer()

        logger.info('sending notifications {0} : {1}'.format(notif_group, notif_message))

        logger.info('notifications kwargs {}'.format(kwargs))

        notif_params = dict(
                type = notif_type,
                message = notif_message,
            )

        if kwargs.get("task_id"):
            notif_params.update(dict(
                        task_id = kwargs.get("task_id")
                    )
                )
        
        async_to_sync( channel_layer.group_send)(notif_group, notif_params )

        return True


    def emit__channel_notification(self):
        """
        notification = dict(
                group
                type
                verb
                message
                task_id
                model
                pk
                uuid
                action
        )
        """
        args = dict(
                group   = self.notifications.get("group", "notifications"),
                type    = self.notifications.get("type", "notification"),
                verb    = self.notifications.get("verb"),
                msg     = self.notifications.get("msg", ""),
                alert   = self.notifications.get("alert", "info"),
                task_id = self.task_id,
                model   = self.model.split(".")[1],
                pk      = self.pk,
                uuid    = self.instance.get("uuid"),
                id      = self.pk,
                name    = self.instance.get("name"),
                action  = self.action,
            )

        channel_layer = get_channel_layer()
        async_to_sync( channel_layer.group_send)(args.get("group"), args )

        return args


