import traceback
import json
from .base_task import *
from django.core.serializers import serialize
from core.models import * #noqa
import ast

_logger = get_task_logger(__name__)


@shared_task(name="ahome.core.RunWorkflowJob",
             ignore_result=False,
             autoretry_for=(Exception,),
             retry_kwargs={'max_retries': 1, 'countdown': 2})
def RunWorkflowJob(*args, **kwargs):
    name = 'Workflow'
    description = 'Workflow Desc'

    _logger.info('RunWorkflowJob executing task id {}'.format(RunWorkflowJob.request.id))

    # _logger.info('Kwargs before {}'.format(kwargs))

    if kwargs:
        kwargs['task_id'] = RunWorkflowJob.request.id

    # _logger.info('Kwargs updated {}'.format(kwargs))
    for step in ['New', 'NewApp']:
        for ds in RunnerTask.objects.filter(state__exact=step):
            # _logger.info(f"RunWorkflowJob output => obj: {ds.obj} pk: {ds.obj_id}")
            obj = get_model_from_str(ds.obj)
            
            try:
                qobj = obj.objects.filter(pk=ds.obj_id)
                for f in qobj:
                    s = serialize('json', [ f ])
                    serializer = json.loads(s)
                    # instance  = serializer[0]

                    instance   = serializer[0]

                    model      = instance.get('model')
                    pk         = instance.get('pk')
                    uuid       = instance.get('fields').get('uuid')
                    name       = instance.get('fields').get('name')


                    if step == 'NewApp':
                        # pass
                        # _logger.info(f"RunWorkflowJob output => instance: { instance }")
                        x = instance.get('fields').get('applications')
                        x = ast.literal_eval(x)
                        apps = [n.strip() for n in x]

                        if model in ['core.iaas']:
                            VirtualMachine.objects.filter(iaas__id=pk).update(applications=apps)
                            vms = VirtualMachine.objects.filter(iaas__id=pk)
                            for vm in vms:
                                s_vm          = serialize('json', [ vm ])
                                serializer    = json.loads(s_vm)
                                instance_vm   = serializer[0]
                                for app in apps:
                                    instance_vm.get('fields').update(dict(kind=app))
                                    runner = BaseTask().run(instance_vm, **kwargs)
                        else:
                            # _logger.info(f"RunWorkflowJob output => NewApp: { apps }")
                            for app in apps:
                                instance.get('fields').update(dict(kind=app))
                                runner = BaseTask().run(instance, **kwargs)

                    else:
                        runner = BaseTask().run(instance, **kwargs)

                # Remove item
                ds.delete()

            except Exception as ex:
                _logger.warning("Exception during RunWorkflowJob task. {}; {}, SKIPPED".format(
                    ex, traceback.format_exc()))
                pass