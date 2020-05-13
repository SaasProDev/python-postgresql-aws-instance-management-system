import re
import uuid

"""
Example of
23b2685429314819aee2e948dd8b4ff8
"""

UUID_LEN = len("23b2685429314819aee2e948dd8b4ff8")


def create_uuid():
    return str(uuid.uuid4())


def unique_id():
    return str(uuid.uuid4()).split('-')[0]


def unique_uuid():
    return "".join(str(uuid.uuid4()).split('-'))


def inject_uuid(data_list):
    for i in data_list:
        i["uuid"] = unique_uuid()
    return data_list


def is_valid_uuid(uuid_to_test):
    UUID_PATTERN = re.compile(r'^[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}$', re.IGNORECASE)
    try:
        return UUID_PATTERN.match(uuid_to_test)
    except:
        return False


def ts_from_uuid1():
    uuid1 = uuid.uuid1()
    return str((uuid1.time - 0x01b21dd213814000) / 1e7)
