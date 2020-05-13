import os
import json
import subprocess
import string
import secrets
from logging import getLogger
from utils import read_text_file_as_lines

import settings

_logger = getLogger(__name__)


def parse_as_ssh(text):
    pids = []
    template = "ssh "

    for line in text.split("\n"):

        if line.startswith("nobody") and line.find(template) > 0:
            params = line.split()

            pid = params[1]
            ppid = params[2]
            started = params[4]
            target = params[-1]

            pids.append({
                'pid': pid,
                'ppid': ppid,
                'target': target,
                'started': started
            })
    return pids


def parse_as_shellinabox(text):
    pids = []
    template = f"{settings.PROXY_EXE}"

    for line in text.split("\n"):
        if line.find(template) > 0:
            params = line.split()
            pid = params[1]
            ppid = params[2]

            started = params[4]
            target = params[15]
            port_str = params[10]
            _, port = port_str.split("=")
            ssh_str = params[14]
            ssh_params = ssh_str.split(":")
            webpath = ssh_params[0][1:]

            sshkey = params[-1] if params[-2] == '-i' else ''

            if ppid == "1":
                continue

            pids.append({
                'ppid': ppid,
                'pid': pid,
                'webpath': webpath,
                'target': target,
                'port': port,
                'sshkey': sshkey,
                'started': started,
                'connect': settings.CONNECT_COMMAND_TEMPLATE.format(port, webpath)
            })
    return pids


def get_started_proxy():
    args = ["ps", "-ef"]

    info = {
        'proxy': [],
        'ssh': []
        }

    with subprocess.Popen(args, stdout=subprocess.PIPE) as proc:
        text = str(proc.stdout.read(), encoding="utf-8")
        info['proxy']   = parse_as_shellinabox(text)
        info['ssh']     = parse_as_ssh(text)

    return info


def kill_process(pids_info):
    result = []
    for info in pids_info:
        command = ["kill", "-9", "{}".format(info.get('pid'))]
        with subprocess.Popen(command, stdout=subprocess.PIPE) as proc:
            result.append(" ".join(command))
    return result


# def _get_inventory_value(uuname, marker):
#     inventory_path = os.path.join(settings.TASK_TMP_ROOT, uuname, "inventory", "hosts")
#     for line in read_text_file_as_lines(inventory_path):
#         idx = line.find(marker)
#         if idx > 0:
#             keyfile_name = line[idx + len(marker):].strip()
#             return keyfile_name
#     return ""
#
#
# def get_sertificate_file_name(uuname):
#     return _get_inventory_value(uuname, "ansible_ssh_private_key_file:")
#
#
# def get_ssh_user_name(uuname):
#     return _get_inventory_value(uuname, "username:")
#
#
# def get_ssh_host(uuname):
#     return _get_inventory_value(uuname, "inventory:")
#
#
def get_random_string(size):
    return ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(size))


current_port = settings.PORTS_RANGE[0]


# todo - check if ports are using
def get_available_port():
    global current_port
    min_port = settings.PORTS_RANGE[0]
    max_port = settings.PORTS_RANGE[1]
    current_port += 1
    if current_port > max_port:
        current_port = min_port
    return current_port


def get_favicon_path(provider='default'):
    icon_name = settings.PROVIDERS_ICONS.get(provider) or settings.PROVIDERS_ICONS.get('default')
    return os.path.join(settings.SHELLINABOX_ASSETS_FOLDER, icon_name)


def json_file(filename, *args, **kwargs):
    with open(filename, "rb") as fh:
        data_as_string = fh.read()
        if isinstance(data_as_string, bytes):
            data_as_string = data_as_string.decode('utf-8', 'ignore')
        return json.loads(data_as_string, *args, **kwargs)

"""    
DATA_EXAMPLE = {
    "id": 1,
    "inventory": "ec2-3-123-153-36.eu-central-1.compute.amazonaws.com",
    "password": "nopass",
    "ssh_key": "/opt/tmp/ssh/tmp0oqp6enb",
    "tags": {
        "Name": "t2",
        "ahome": "9c1dfa5c-a3db-4cea-af18-380e8733b892",
        "instance_name": "t2"
    },
    "username": "ec2-user",
    "uuid": "e6d49f94-07c0-4ebf-a25c-fe88370d676d"
}
"""

"""
+ **beep.wav** audio sample that gets played whenever the terminal BEL is sounded.
+ **favicon.ico** favicon image file that is displayed in the browser's navigation bar.
+ **ShellInABox.js** JavaScript file implementing the AJAX terminal emulator.
+ **styles.css** CSS style file that controls the visual appearance of the terminal.
+ **print-styles.css** CSS style file that controls the  visual  appearance of printed pages when using the VT100 transparent printing feature.
"""


def start_proxy(host=None, user=None, port=None, webpath=None, uuid=None, certificate_path=None, **kwargs):
    if not host and not uuid:
        raise Exception(f"Invalid paramaters. 'host={host}'; 'user={user}';  'uuid={uuid}'")

    if uuid:
        vm_connect_info = json_file(os.path.join(settings.AHOME_PROOT_BASE_PATH, "vm/vm.{}.json".format(uuid)))

        host = host or vm_connect_info['inventory']
        user = user or vm_connect_info['username']

        ssh_key_filename = vm_connect_info['ssh_key']
    else:
        ssh_key_filename = certificate_path

    port = port or get_available_port()
    webpath = webpath or get_random_string(size=settings.RANDOM_PATH_LENGTH)
    pidfile = f"{settings.PIDFILE_DIRECTORY}/{webpath}.{get_random_string(4)}.pid"

    favicon_path = get_favicon_path()

    args = [settings.PROXY_EXE,
            f"--background={pidfile}",
            f"--cert={settings.CERTIFICATE_FOLDER}",
            f"--port={port}",
            f"--static-file={favicon_path}:favicon.ico",
            f"--disable-ssl",
            f"--disable-ssl-menu",
            f"--user={settings.SERVER_USER_PID}",
            f"--group={settings.SERVER_GROUP_PID}",
            f"--service",
            f"/{webpath}:{settings.PROXY_USER_NAME}:{settings.PROXY_GROUP_NAME}:HOME:/usr/bin/ssh {user}@{host}"
            ]
    if uuid:
        args[-1] += f" -i {ssh_key_filename}"

    _logger.debug("Command: '{}' STARTING...".format(" ".join(args)))
    subprocess.call(args)
    # _logger.debug("STARTED.")

    return {
        "webpath": webpath,
        "pidfile": pidfile,
        "port": port,
        "connect": settings.CONNECT_COMMAND_TEMPLATE.format(port, webpath)
        }

