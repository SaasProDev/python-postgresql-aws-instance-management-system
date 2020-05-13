from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from celery.utils.log import get_task_logger
from celery import shared_task


logger = get_task_logger(__name__)


@shared_task(name="ahome.core.send_notification")
def send_notification(notif_group, notif_type, notif_message, sender=None):
    sender = sender or {}
    channel_layer = get_channel_layer()

    logger.info('sending notifications {0} : {1}'.format(notif_group, notif_message))

    notif_params = dict(type=notif_type, message=notif_message)

    if sender.get("task_id"):
        notif_params.update(dict(task_id=sender.get("task_id")))

    async_to_sync(channel_layer.group_send)(notif_group, notif_params)

    return True
