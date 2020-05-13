from .base_task import *

logger = get_task_logger(__name__)


# @shared_task(name="ahome.core.RunStartJob", ignore_result=False, autoretry_for=(Exception,), exponential_backoff=2, retry_kwargs={'max_retries': 5}, retry_jitter=False)
@shared_task(name="ahome.core.RunStartJob", ignore_result=False, autoretry_for=(Exception,), retry_kwargs={'max_retries': 1, 'countdown': 2})
def RunStartJob(instance, **kwargs):
    name = 'RunStartJob'
    description = 'RunStartJob Desc'

    logger.info('RunStartJob executing task id {}'.format(RunStartJob.request.id))

    # logger.info('Kwargs before {}'.format(kwargs))

    #if kwargs:
    kwargs['task_id'] = RunStartJob.request.id

    # logger.info('Kwargs updated {}'.format(kwargs))

    runner = BaseTask().run(instance, **kwargs)

    logger.info(f"Final runner output => \nstatus: {runner.status} rc: {runner.rc}")
    logger.info(f"Final runner output : \n{runner.status}")

    if runner.rc > 0:
        # pass
        logger.info(f"LOG KWARGS: \nretry: {RunStartJob.request.retries} on {RunStartJob.retry_kwargs}")
        if int(RunStartJob.request.retries) < int(RunStartJob.retry_kwargs.get('max_retries')):
            raise Exception(f'Runner {runner.status} returned unexpected response code: {runner.rc}')

        RunStartJob.update_state(state=states.FAILURE)
