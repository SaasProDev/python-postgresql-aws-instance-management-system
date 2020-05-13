# Python
import contextlib
import logging
import threading
import json
import pkg_resources
import sys


# Django
from django.conf import settings
from django.db.models.signals import (
    pre_save,
    post_save,
    pre_delete,
    post_delete,
    m2m_changed,
)
from django.dispatch import receiver
from django.contrib.auth import SESSION_KEY
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from core.models import * #noqa
from core.tasks import *
from celery import chain

import netaddr
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import copy
from django.core.serializers import serialize

from rest_framework.authtoken.models import Token


import paramiko
from binascii import hexlify
from Crypto.PublicKey import RSA
import io
from django.core.files.base import ContentFile
from logging import getLogger



_logger = getLogger(__name__)

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create__auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

post_save.connect(create__auth_token, sender=settings.AUTH_USER_MODEL)




# def emit_update_sdn_on_created_or_deleted(sender, **kwargs):
#     instance = kwargs['instance']
#     created = kwargs['created']
    
#     if created:
#         # RunLibvirtJob.apply_async(ignore_result=False)
#         print ("SDN instance created : {}".format(created))
#         pass
#     print (instance.id)


# post_save.connect(emit_update_sdn_on_created_or_deleted, sender=Sdn)




# post_save.connect(create_activity_item, sender=Status,
#                   dispatch_uid="create_activity_item")

# ahome-core    | signal
# ahome-core    | created
# ahome-core    | update_fields
# ahome-core    | raw
# ahome-core    | using


#TODO -- move it to utils and share it in views and signals

def schedule__runner_task(obj):

    # Provider.objects.create(provider=instance)
#TODO - To fix    
    try:
        s = serialize('json', [ obj ])
        serializer = json.loads(s)

        instance = serializer[0]

        model = instance.get('model')
        pk    = instance.get('pk')
        uuid  = instance.get('fields').get('uuid')
        

        # _logger.info( "model: {} pk: {} uuid: {} instance: ---".format(model, pk, uuid) )

        entry = dict(
            obj    = model,
            obj_id = pk,
            state  = 'New',
            ident  = uuid,  
            )
        runner_obj = RunnerTask.objects.filter( **entry )
        if not runner_obj:
            RunnerTask.objects.create(**entry)

    except Exception as e:
        # raise e
        _logger.warning("FIX ME PLEASE", str(e))

    


    # runner_obj = RunnerTask.objects.filter( state  = 'New' )
    # for r in runner_obj:
    #     _logger.info( "Start processing record: obj {} - id {}".format(r.obj, r.id ) )
    #     r.state = 'Running'
    #     r.save(update_fields=['state'])
    #     # process
    #     # ...
    #     _logger.info( "Stop processing record: obj {} - id {}".format(r.obj, r.id ) )
    #     r.state = 'Terminated'
    #     # r.delete()
    #     r.save(update_fields=['state'])



    # RunActivateJob1.delay(instance=instance)








def run__job_on_create(obj):

    # Provider.objects.create(provider=instance)
    s = serialize('json', [ obj ])
    serializer = json.loads(s)

    instance = serializer[0]

    # model = instance.get('model')
    # uuid = instance.get('fields').get('uuid')
    # name = instance.get('fields').get('name')

    RunActivateJob1.delay(instance=instance)


def just_report(sender, **kwargs):
    """
    Just a TEST signal - for development purposes now
    :param sender:
    :param kwargs:
    :return:
    """
    _logger.debug("ResourceAliveHistory Committed - JUST INFO FOR NOW", kwargs)
    # _logger.info("POST SAVE  *** ResourceAliveHistory*** Sender: {}".format(sender))
    pass


def emit__startjob_iaas_on_create(sender, **kwargs):
    _logger.info("POST SAVE  *** IaaS ***")
    created = kwargs['created']
    instance = kwargs['instance']

    schedule__runner_task(instance)

    if created:
        run__job_on_create(instance)
        

def emit__startjob_virtualmachine_on_create(sender, **kwargs):
    _logger.info("POST SAVE  *** VM ***")
    created = kwargs['created']
    instance = kwargs['instance']
    _logger.info( "VirtualMachine Updated: {}".format(instance) )
    schedule__runner_task(instance)
    # if created:
    #     # run__job_on_create(instance)
    #     # schedule__runner_task(instance)
    #     pass








# post_save.connect(emit__generate_rsa_key_on_save, sender=IaaS)

post_save.connect(emit__startjob_iaas_on_create, sender=IaaS)

post_save.connect(emit__startjob_virtualmachine_on_create, sender=VirtualMachine)

post_save.connect(just_report, sender=ResourceAliveHistory)

# post_save.connect(emit__generate_rsa_key_on_save, sender=UserSecret)



# @receiver(post_save, sender=VirtualMachine)
# def create_virtualmachine_config(sender, instance, created, **kwargs):
#     if created:
#         # Provider.objects.create(provider=instance)
#         print("signal create for new Virtual Machine")




# post_save.connect(emit__startjob_iaas_on_create, sender=IaaS)

# post_save.connect(emit__startjob_virtualmachine_on_create, sender=VirtualMachine)

# # post_save.connect(emit__generate_rsa_key_on_save, sender=UserKey)

# post_save.connect(emit__generate_rsa_key_on_save, sender=UserSecret)

# @receiver(post_save, sender=IaaS)
# def save_iaas_config(sender, instance, **kwargs):
#     # instance.profile.save()
#     print ("signal - IaaS updated")

#     # channel_layer = get_channel_layer()
    
#     # async_to_sync(channel_layer.group_send)("notifications", {
#     #     "type": "notification",
#     #     "message": "Hello there!  - from signals",
#     #     })



#     # create_random_virtual_machines.delay(50)
#     # job = RunJob()
#     # job.start(cmd='ping')
    
#     # RunJob.delay()
#     # RunJob.apply_async(ignore_result=False)





# #TODO: temporary - trigger launch from Provider add/update
# @receiver(post_save, sender=Provider)
# def save_provider_config(sender, instance, **kwargs):

#     # RunLibvirtJob.apply_async(ignore_result=False)
#     pass






