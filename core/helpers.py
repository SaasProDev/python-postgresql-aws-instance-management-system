from .models import ResourceAliveHistory

import logging
_logger = logging.getLogger(__name__)

# model = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
# resource_id = models.PositiveIntegerField(db_index=True)
# resource_status = models.CharField(max_length=4, choices=RESOURCE_STATUS_CHOICES)
#
# task_id = models.PositiveIntegerField()
# task_mode = models.CharField(max_length=MAX_TASK_NAME_LENGTH)
#
# task_initialised = models.DateTimeField(auto_now_add=True)
# task_completed = models.DateTimeField(auto_now=True)

# self.action, self.model, self.pk, self.task_id, life_cycle


POSSIBLE_LIFE_CYCLES = ("start", "finish",)

#
# def run_check(self, request, pk=None):          return self._run('check', "Synchronization")
# def run_synchronize(self, request, pk=None):    return self._run('check', 'Synchronization')
# def run_activate(self, request, pk=None):       return self._run('start', 'Activation')
# def run_deactivate(self, request, pk=None):     return self._run('stop', 'Deactivation')
# def run_reconfigure(self, request, pk=None):    return self._run('reconfigure', 'Reconfiguration')
# def run_shutdown(self, request, pk=None):       return self._run('stop', 'Shutting down')
# def run_deployment(self, request, pk=None):     return self._run('deploy', 'Deployment')
# def run_decommission(self, request, pk=None):   return self._run('remove', 'Decommission')
#
# TASKS_LIFE_CYCLES = {
#     'check'
# }



def commit_alive_event(action:str, model: str, resource_id: int, task_id: int, life_cycle: str):
    if life_cycle not in POSSIBLE_LIFE_CYCLES:
        mess = "Invalid life_cycle: '{}'. It must be from this list: {}".format(life_cycle, POSSIBLE_LIFE_CYCLES)
        _logger.error(mess)
        raise Exception(mess)

    content_type = ResourceAliveHistory.get_content_type(model)

    if not content_type:
        mess = "Invalid model: '{}'".format(model)
        _logger.error(mess)
        raise Exception(mess)
    try:
        # status = "up" if action in ("start", ) else ""
        ResourceAliveHistory.objects.create(model=content_type,
                                            resource_id=resource_id,
                                            resource_status=action,
                                            task_id=task_id,
                                            task_mode=action)
    except Exception as ex:
        _logger.error("Cannot save ResourceAliveHistory item. "
                      "Model: '{}'; resource: '{}' Exception: {}".format(model, resource_id, ex))
        raise
