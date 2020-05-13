"""
Set of utils for time manipulation
"""

from datetime import timezone, timedelta
import time, datetime
# import time


from dateutil import parser


_default_format_datetime = '%Y-%m-%d %H:%M:%S'


def time_as_string(time_val=None, time_fmt=None):
    """ Returns time in form 'YYYY-MM-DD hh:mm:ss'
    :param timeval:  datetime
    :param time_fmt: str @example '%Y-%m-%d %H:%M:%S'
    """

    time_val = time_val or datetime.datetime.now()
    time_fmt = time_fmt or _default_format_datetime

    # assert(issubclass(type(time_val), datetime))

    return time_val.strftime(time_fmt)


def timestamp(future_seconds=0):
    return time.time() + int(future_seconds)


def hour_subtract(same_date, hours):
    return same_date - timedelta(hours=hours)


def from_timestamp(time_stamp, divide=None):
    time_stamp = int(time_stamp)
    if divide:
        time_stamp = int(time_stamp / divide)
    return datetime.datetime.fromtimestamp(time_stamp)


def diff_to_now(data_str):
    return ""
    # if not data_str:
    #     return None
    # data_str = data_str.split(".")[0]
    # print("*** DATE 0: [{}]".format(data_str))
    #
    # date = from_timestamp(data_str)
    # print("*** DATE 1: [{}]".format(date))
    # delta = date - time.time()
    # print("*** DATE 2: [{}]".format(delta))
    # return delta
    # #


def seconds_as_date(time_in_sec):
    return str(timedelta(seconds=time_in_sec))


def time_delta_in_human_view(time1, time2):
    return seconds_as_date(abs(time1 - time2))


INTERVALS = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
    )


def display_time(seconds, granularity=2):
    result = []

    for name, count in INTERVALS:
        value = int(seconds // count)
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])


def sting_to_date(date_str):
    return parser.parse(date_str)


def date_time_now():
    local_timezone = datetime.datetime.now(timezone.utc).astimezone(timezone.utc).tzinfo
    date_time_now = datetime.datetime.now(local_timezone.utc)
    return date_time_now
