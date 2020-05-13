"""
Copyright tretyak@gmail.com
https://github.com/xmig/celerytasks

see https://docs.celeryproject.org/en/latest/userguide/calling.html
    https://pawelzny.com/python/celery/2017/08/14/celery-4-tasks-best-practices/

"""
import time
import collections
import traceback
from celery import Task
from celery import shared_task
from celery import chain
from celery.result import AsyncResult
from abc import ABCMeta, abstractmethod
from sysutils.utils.reflection_utils import class_by_name

from .app import celery_app

from logging import getLogger
_logger = getLogger(__name__)


def cut_of(datastr, max_size=128):
    try:
        return datastr if len(datastr) < max_size else datastr[:max_size] + "..."
    except:
        return datastr


def xprint(datastr, max_size=128):
    print(cut_of(datastr, max_size))


class TraceTask(Task):
    """ Just a Trace Task support - any real functionality for now
    """
    abstract = True
    mess_prefix = "Task"

    def message(self, mess_template, retval_or_einfo):
        xprint((mess_template.format(
            self.mess_prefix,
            self.request.task,
            self.request.id,
            self.request.args,
            retval_or_einfo)))

    def on_success(self, retval, task_id, args, kwargs):
        return self.message("{} OK    '{}' Id: '{}' Params {} Result: [{}]", retval)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        return self.message("{} ERROR '{}' Id: '{}' Params {} Result: [{}]", einfo)


class TraceTaskLinked(TraceTask):
    mess_prefix = "Linked Task"


def __perform(performer, *args, **kwargs):
    """
    Perform a particular task. Support conditional/repeated Tasks
    Provides start/stop Task tracing info
    :param performer: <AsyncTask>
    :return: nothing
    """
    assert (isinstance(performer, AsyncTask))

    max_count = performer.repeat_maxcount()
    while max_count > 0:
        max_count -= 1

        name = performer.__class__.__name__
        task_id = performer.get_task_id()

        xprint("### Task: '{}' id='{}' stating...".format(name, task_id))
        result = performer.perform(*args, **kwargs)
        if not performer.is_conditional() or performer.check_condition(result):
            xprint(("### Task RESULT: [{}]".format(result)))
            return result
        timeout = performer.repeat_timeout()
        xprint("### Conditional task repeated. Task: '{}' id='{}'; Timeout: [{}] sec; Can be repeated [{}] times".format(
            name, task_id, timeout, max_count))
        time.sleep(timeout)

@shared_task
@celery_app.task
def periodic_task_performer(task_class_name):
    xprint("Periodic Task '{}' starting...".format(task_class_name))
    cls = class_by_name(task_class_name)
    cls().perform()


def linked_task_itself(self, result, performer):
    """ Runs a linked task
    :param result: <Any> result of the previous joined Task
    :param performer: <AsyncTask> Task which really will be performed
    """
    performer.set_request(self.request)
    return __perform(performer, result)


@celery_app.task(base=TraceTaskLinked, bind=True)
def linked_task_receive(self, result, performer):
    """ Function started USING decorator (in case of RECEIVING a TASK) """
    return linked_task_itself(self, result, performer)


def linked_task_send(self, result, performer):
    """ Function started WITHOUT decorator (in case of SENDING TASK) """
    return linked_task_itself(self, result, performer)


def dynamic_linked_task(channel):
    dtask = celery_app.task(base=TraceTaskLinked, bind=True, channel=channel)
    linked_task_send.__name__ = "linked_task_receive"
    return dtask(linked_task_send)


def start_task_itself(self, performer, *args, **kwargs):
    """
    SERVER SIDE
    Runs Task Asynchronous
    :param performer: <AsyncTask> Task which really will be performed
    """
    from pprint import pprint

    print("*****")
    pprint(performer, indent=4)
    print("*****")

    performer.set_request(self.request)
    result = __perform(performer, *args, **kwargs)
    return result


def start_task_send(self, performer, *args, **kwargs):
    """
    CLIENT SIDE
    Function started WITHOUT decorator (in case of SENDING TASK) """
    return start_task_itself(self, performer, *args, **kwargs)


@celery_app.task(base=TraceTask, bind=True)
def start_task_receive(self, performer, *args, **kwargs):
    """
    SERVER SIDE
    Function started USING decorator (in case of RECEIVING a TASK) """
    return start_task_itself(self, performer, *args, **kwargs)


def dynamic_task(channel):
    dtask = celery_app.task(base=TraceTask, bind=True, channel=channel)
    start_task_send.__name__ = "start_task_receive"
    return dtask(start_task_send)


def get_result_by_ids(task_ids):
    """ Check if tasks are completed
    :param task_ids: list of 'task_id'
    :return: 2 values: "count_of_ready_tasks", "list of dicts {'task_id': 'task_result'(or None)}"
    """
    assert(isinstance(task_ids, collections.Iterable))
    ready = 0
    result_dict = {}
    for task_id in task_ids:
        result = get_result_by_id(task_id)
        ready = ready + 1 if result else ready
        result_dict[task_id] = result

    return ready, result_dict


def get_result_by_id(task_id):
    """Returns result from a queue
    """
    task = AsyncResult(task_id, backend=celery_app.backend)
    try:
        return task.result if task.successful() else None
    except Exception as ex:
        xprint("EXCEPTION DURING TASK PROCESSING {}".format(ex))
        return None


class DummyResult(object):
    """ Base class for unspecified results or errors
    """
    def __str__(self):
        return ""


class EmptyResult(DummyResult):
    """ Detect the Task successfully completed but result for this particular Task do not supposed
    """
    pass


class ErrorResult(DummyResult):
    """ Task completer with ERROR
    """
    def __init__(self, mess):
        self.mess = mess

    def __str__(self):
        return self.mess


class ContextHolder(object):
    """
    @see http://celery.readthedocs.org/en/latest/userguide/tasks.html?highlight=requestcontext#context
    """
    def __init__(self):
        self.request = None

    def context(self):
        return self.request

    def set_request(self, request):
        self.request = request

    def get_task_id(self):
        return self.request.id


class AsyncTask(ContextHolder, metaclass=ABCMeta):
    repeat_timeout_value = 1
    repeat_maxcount_value = 100

    def __init__(self, channel="default"):
        self.result_holder = None
        self.joined = []
        self.channel = channel
        super(AsyncTask, self).__init__()

    @property
    def __xdict__(self):
        return {"aaaaaaaaaaaaaaaaaaaaaaaaaaa": 100}
        pass

    def set_channel(self, channel):
        self.channel = channel

    @classmethod
    def empty_result(cls):
        return EmptyResult()

    @classmethod
    def ok_result(cls):
        return EmptyResult()

    @classmethod
    def error_result(cls, mess):
        return ErrorResult(mess)

    @classmethod
    def is_empty_result(cls, result):
        return isinstance(result, EmptyResult)

    @classmethod
    def is_error_result(cls, result):
        return isinstance(result, ErrorResult)

    @classmethod
    def is_dummy_result(cls, result):
        return issubclass(result.__class__, DummyResult)

    @staticmethod
    def result_by_id(task_id):
        """Returns result from a queue
        """
        return get_result_by_id(task_id)

    def __call__(self, *args, **kwargs):
        return self.perform(*args, **kwargs)

    def join(self, *tasks):
        """ Add sub task(s) to the current Task
        :param tasks: <Task | list of Tasks> Tasks which will be "joined" as sub tasks
        :return: <self>
        """
        for task in tasks:
            self.joined.append(task)
        return self

    @staticmethod
    def is_conditional():
        return False

    def repeat_timeout(self):
        """ Repeat timeout in secs for 'conditional' tasks
        Usually should be overrated
        :return: <int>
        """
        return self.repeat_timeout_value

    def repeat_maxcount(self):
        """ Max cunt the particular Task would be repeated.
        For 'conditional' tasks
        Usually should be overrated
        :return: <int>
        """
        return self.repeat_maxcount_value

    def check_condition(self, value):
        raise Exception("Method must me overrated")

    def go(self, asynchronous, *args, **kwargs):
        if asynchronous:
            return self.run(*args, **kwargs)
        else:
            return self.perform(*args, **kwargs)

    def run(self, *args, **kwargs):
        """Really starts a task
        *args, **kwargs - are parameters for 'perform'
        """
        try:
            #task_args = self.__dict__
            if not self.joined:
                self.result_holder = dynamic_task(self.channel).s(self, *args, **kwargs).apply_async()
                #self.result_holder = dynamic_task(self.channel).delay(self, *args, **kwargs)
            else:
                sub_tasks = []
                for jt in self.joined:
                    sub_tasks.append(dynamic_linked_task(self.channel).s(jt))
                self.result_holder = chain(dynamic_task(self.channel).s(self, *args, **kwargs), *sub_tasks).apply_async()
        except Exception as ex:
            print(traceback.format_exc())
            _logger.warning("Cannot Run Task '{}'; Exception: {}; {}".format(self, ex, traceback.extract_stack()))
            pass
        return self

    @abstractmethod
    def perform(self, *args, **kwargs):
        raise Exception("Abstract method must me overrated")

    @property
    def task_id(self):
        return self.result_holder.id if self.result_holder else None

    @property
    def result(self):
        """
        :return: <any|None> Returns Task result value
        In case this is a "joined" task - real result is a result or the "LAST" sub task
        """
        if self.successful():
            return self.result_holder.result
        return None

    @property
    def result_chain(self):
        """
        :return: <list|None> list of all results for a chain
            in order from the parent task to a last sub task
        """
        if self.successful():
            result = [self.result]
            parent = self.result_holder.parent
            while parent:
                result.append(parent.get())
                parent = parent.parent
            return result[::-1]
        return None

    def is_completed(self):
        return self.ready()

    def ready(self):
        return self._result_task_param('ready')

    def successful(self):
        return self._result_task_param('successful')

    def failed(self):
        return self._result_task_param('failed')

    def _result_task_param(self, param_name):
        if self.result_holder:
            return getattr(self.result_holder, param_name)()
        return None


class TaskKindWrapper(AsyncTask):
    def __init__(self, task_name: str, performer: AsyncTask, **kwargs):
        self.task_name = task_name
        self.performer = performer
        super().__init__(**kwargs)

    def perform(self, *args, **kwargs):
        return {"task_name": self.task_name, "task_result": self.performer.perform(*args, **kwargs)}

