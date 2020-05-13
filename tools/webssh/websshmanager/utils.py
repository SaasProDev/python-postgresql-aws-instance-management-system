import os, io
import datetime

from logging import getLogger
_logger = getLogger(__name__)

_default_format_datetime = '%Y-%m-%d-%H:%M:%S'


def time_as_string(time_val=None, time_fmt=None):
    time_val = time_val or datetime.datetime.now()
    time_fmt = time_fmt or _default_format_datetime
    return time_val.strftime(time_fmt)


def full_file_name(file_name, folder=None, extension=None):
    file_name = file_name if folder is None else os.path.join(str(folder), file_name)
    file_name = file_name if extension is None else "{}.{}".format(file_name, extension)
    return file_name


def write_text_file(data, file_name, folder=None, extension=None, mode='wb'):
    try:
        file_name = full_file_name(file_name, folder, extension)
        with io.open(file_name, mode) as file_stream:
            if isinstance(data, str):
                data = bytes(data.encode('utf-8'))
            file_stream.write(data)
    except Exception as ex:
        raise
    else:
        return file_name

def split_path(path):
    allparts = []
    while True:
        parts = os.path.split(path)
        if parts[0] == path:
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path:
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts


def check_or_create_folder(path, skip_last_part=False):
    path = os.path.normpath(os.path.abspath(path))
    parts = split_path(path)
    parts = parts[:-1] if skip_last_part else parts
    for i, item in enumerate(parts):
        temp_parts = parts[0: i + 1]
        temp_name = '/'.join(temp_parts)[1:]
        if temp_name and not os.path.exists(temp_name):
            try:
                os.mkdir(temp_name)
            except OSError as er:
                raise
    return path


def list_folder(folder_name):
    try:
        return os.listdir(folder_name) if os.path.exists(folder_name) else []
    except Exception as e:
        raise


def read_text_file_as_lines(filename, folder=None):
    filename = filename if not folder else os.path.join(folder, filename)
    with open(filename, "rt", encoding="utf-8") as f:
        lines = [line.rstrip('\n') for line in f.readlines()]
    return lines


def delete_file(file_name, raise_if_no_file=False):
    try:
        os.remove(file_name)
    except FileNotFoundError:
        if raise_if_no_file:
            raise
