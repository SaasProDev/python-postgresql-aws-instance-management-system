from .base_task import *
from celery import chain

import traceback
import json
from django.core.serializers import serialize
from core.models import * #noqa
import ast


logger = get_task_logger(__name__)


# @shared_task(name="ahome.core.RunActivateJob1", ignore_result=False, autoretry_for=(Exception,), exponential_backoff=2, retry_kwargs={'max_retries': 5}, retry_jitter=False)
@shared_task(name="ahome.core.RunActivateJob1", ignore_result=False, autoretry_for=(Exception,), retry_kwargs={'max_retries': 1, 'countdown': 2})
def RunActivateJob1(instance, **kwargs):
    from .run_start_job_task import RunStartJob
    from .run_workflow_task import RunWorkflowJob

    name = 'RunActivateJob1'
    description = 'RunActivateJob1 Desc'

    logger.info('RunActivateJob1 Executing task id {}'.format(RunActivateJob1.request.id))

    job_type       = instance.get('model')

    logger.info('JOB TYPE {}'.format(job_type))

    if job_type in ['core.usercredential']:

        pk       = instance.get('pk')
        logger.info('RUN JOB {} - {}'.format(job_type, pk))

        runner = BaseTask().run(instance, **kwargs)

    elif job_type in ['core.iaas']:

        pk       = instance.get('pk')
        logger.info('RUN JOB {} - {}'.format(job_type, pk))
        
        runner = BaseTask().run(instance, **kwargs)

        for ds in VirtualMachine.objects.filter(iaas__id=pk):
            
            s = serialize('json', [ ds ])
            serializer = json.loads(s)
            instance_vm   = serializer[0]

            logger.info('RUN VIRTUAL MACHINE JOB {} - {}'.format(instance_vm.get('model'), instance_vm.get('pk') ))
            runner = BaseTask().run(instance_vm, **kwargs)

            # isinstance(tmpDict[key], list)
            apps = instance.get('fields').get('applications', [])
            if not isinstance(apps, list):
                apps = ast.literal_eval(apps)
                apps = [n.strip() for n in apps]

            logger.info('RUN JOB APPS {} - {} - ** {} **'.format(job_type, pk, apps ))

            for app in apps:
                # logger.info('RUN JOB APPS {} - {} - ** {} **'.format(job_type, pk, app ))
                instance_vm.get('fields').update(dict(kind=app))
                runner = BaseTask().run(instance_vm, **kwargs)



    elif job_type in ['core.virtualmachine']:

        pk       = instance.get('pk')
        logger.info('RUN JOB {} - {}'.format(job_type, pk))

        runner = BaseTask().run(instance, **kwargs)

        apps = instance.get('fields').get('applications', [])
        if not isinstance(apps, list):
            apps = ast.literal_eval(apps)
            apps = [n.strip() for n in apps]

        for app in apps:
            instance.get('fields').update(dict(kind=app))
            runner = BaseTask().run(instance, **kwargs)




    else:

        pk       = instance.get('pk')
        logger.info('RUN JOB {} - {}'.format(job_type, pk))

        runner = BaseTask().run(instance, **kwargs)




    # res = chain(RunStartJob.si(instance, **kwargs) | RunWorkflowJob.si()).apply_async()




    # res = RunStartJob.si(instance, **kwargs).apply_async()


    # logger.info('Chain result \n{}'.format(res)

    # runner = BaseTask().run(instance, **kwargs)

    # logger.info(f"Final runner output => \nstatus: {runner.status} rc: {runner.rc}")

    # logger.info(f"Final runner output : \n{runner.status}")
    # if runner.rc > 0:
    #     # pass
    #     logger.info(f"LOG KWARGS: \nretry: {RunActivateJob1.request.retries} on {RunActivateJob1.retry_kwargs}")
    #     if int(RunActivateJob1.request.retries) < int(RunActivateJob1.retry_kwargs.get('max_retries')):
    #         raise Exception(f'Runner {runner.status} returned unexpected response code: {runner.rc}')

    #     RunActivateJob1.update_state(state=states.FAILURE)

