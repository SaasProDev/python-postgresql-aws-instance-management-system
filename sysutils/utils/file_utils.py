"""
copyright tretyak@gmail.com
Set of Input / Output utilities
"""

import os
import io
import shutil
import glob
import random
import string

from functools import partial


def full_file_name(file_name, folder=None, extension=None):
    file_name = file_name if folder is None else os.path.join(str(folder), file_name)
    file_name = file_name if extension is None else "{}.{}".format(file_name, extension)
    return file_name


def file_extension(file_name):
    name, extension = os.path.splitext(file_name)
    return extension[1:] if extension and len(extension) > 1 else None


def split_path2(path):
    path_parts = []
    while path != os.path.dirname(path):
        path_parts.append(os.path.basename(path))
        path = os.path.dirname(path)
        path_parts.reverse()
    return path_parts


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


def part_of_path(path, start_from, stop_to):
    parts = split_path(path)
    return '/'.join(parts[start_from:stop_to])


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


def move_folder_from_to(source, destination):
    return shutil.move(source, destination)


def file_rename(old_name, new_name):
    return shutil.move(old_name, new_name)


def delete_file(file_name, raise_if_no_file=False):
    try:
        os.remove(file_name)
    except FileNotFoundError:
        if raise_if_no_file:
            raise


def list_folder(folder_name):
    try:
        return os.listdir(folder_name) if os.path.exists(folder_name) else []
    except Exception as e:
        raise


def random_file_name(file_ext=None, name_size=16):
    name = ''.join([random.choice(string.ascii_lowercase) for _ in range(name_size)])
    return "{}.{}".format(name, file_ext) if file_ext else name


def get_file_names(file_mask, folder="./"):
    mask = os.path.join(folder, file_mask)
    return sorted([x for x in glob.glob(mask)])


def read_file(file_name, folder=None, extension=None, mode='rb'):
    try:
        file_name = full_file_name(file_name, folder, extension)
        with open(file_name, mode) as file_stream:
            return file_stream.read()
    except Exception as ex:
        raise


def read_file_as_utf8(full_file_name):
    with open(full_file_name, "rb") as h:
        text = str(h.read(), 'utf-8')
        return text


def read_text_file(file_name, folder=None, extension=None):
    return str(read_file(file_name, folder, extension, mode='rt'))


def read_text_file_as_lines(filename, folder=None):
    filename = filename if not folder else os.path.join(folder, filename)
    with open(filename, "rt", encoding="utf-8") as f:
        lines = [line.rstrip('\n') for line in f.readlines()]
    return lines


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


def write_binary_file(data, file_name=None, folder=None, extension=None):
    try:
        file_name = file_name or random_file_name(file_name)
        file_name = full_file_name(file_name, folder, extension)
        with io.open(file_name, 'wb') as file_stream:
            file_stream.write(data)
    except Exception as ex:
        raise
    else:
        return file_name


def get_filename(full_filename):
    return os.path.basename(full_filename)


def get_basename(filename):
    name = os.path.basename(filename)
    return os.path.splitext(name)[0]


def get_folder(full_name):
    return os.path.split(full_name)[0]


def get_ext(filename):
    """
    return string after the LAST dot (include ".")
    For example for "hello.word.json" it will be  ".json"
    :param filename: <str> full path or base name file name
    :return: <str>
    """
    name = os.path.basename(filename)
    return os.path.splitext(name)[1]


def get_long_ext(filename):
    """
    return string after the FIRTS dot (include ".")
    For example for "hello.word.json" it will be  ".word.json"
    :param filename: <str> full path or base name file name
    :return: <str>
    """
    name = os.path.basename(filename)
    idx = name.index(".")
    return name[idx:]


def make_filename_link(source, target):
    return os.link(source, target)


def is_file_exists(path, folder=None):
    path = path if not folder else os.path.join(folder, path)
    return os.path.exists(path)


def walk(root: str = './', perform: callable = None, followlinks: bool = False):
    for path, folders, files in os.walk(root, followlinks=followlinks):
        for folder in folders:
            walk(folder, perform, followlinks)
        for file in files:
            perform(path, file)
