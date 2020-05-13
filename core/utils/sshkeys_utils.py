import os, stat
from logging import getLogger
from django.conf import settings

import io, tempfile, errno
from io import StringIO

import paramiko
from binascii import hexlify
from Crypto.PublicKey import RSA

from distutils.version import LooseVersion as Version

_logger = getLogger(__name__)

import os
import errno
import stat
import tempfile
import subprocess
# import piramiko
# from core.utils.common import get_ssh_version
from distutils.version import LooseVersion as Version
from django.utils.encoding import smart_str
from .memoize import memoize


OPENSSH_KEY_ERROR = u'''\
It looks like you're trying to use a private key in OpenSSH format, which \
isn't supported by the installed version of OpenSSH on this instance. \
Try upgrading OpenSSH or providing your private key in an different format. \
'''

@memoize()
def get_ssh_version():
    """
    Return SSH version installed.
    """
    try:
        proc = subprocess.Popen(['ssh', '-V'], stderr=subprocess.PIPE)
        result = smart_str(proc.communicate()[1])
        return result.split(" ")[0].split("_")[1]
    except Exception:
        return 'unknown'


def new_ssh_key_pair(key_kind: str, length: int, password: str):
    buffer = io.StringIO()
    try:
        if key_kind == 'rsa':
            private_key_obj = paramiko.RSAKey.generate(length)
        elif key_kind == 'dsa':
            private_key_obj = paramiko.DSSKey.generate(length)
        else:
            raise Exception('SSH private key must be `rsa` or `dsa`')
        if password:
            private_key_obj.write_private_key(buffer, password=password)
        else:
            private_key_obj.write_private_key(buffer, password=None)

        return private_key_obj, buffer.getvalue()
    except IOError:
        _logger.error('These is error when generate ssh key.')
        raise


# todo key_kind - detect automatically
def existed_ssh_key_pair(private_key: str, key_kind: str = "rsa", password=None):
    buffer = io.StringIO(private_key)
    private_key_obj = paramiko.RSAKey.from_private_key(buffer, password) if key_kind == 'rsa' \
        else paramiko.DSSKey.from_private_key(buffer, password)
    return private_key_obj, buffer.getvalue()


def load_ssh_from_database(uuid):
    inputs = load_privatekey_from_db(uuid)

    if not inputs:
        return None, None, None, None

    keykind = inputs.get('keykind')
    passphrase = inputs.get('passphrase')
    privatekey = inputs.get('privatekey')
    publickey =  inputs.get('publickey')

    if privatekey and publickey:
        return privatekey, publickey, keykind, passphrase
    if privatekey:
        private_key_obj, private_key = existed_ssh_key_pair(privatekey)
        return private_key, private_key, None, None
    if publickey:
        return None, publickey, keykind, passphrase

    return None, None, None, None


# TODO: change the path to a secure workspace
# TODO: THIS CODE SHOULD NOT BE INVOKED DURING **SAVE** Database Object - Please APPLY Lazy Loading
def generate_inputs_sshkeys(inputs):
    from .common import is_valid_uuid
    _logger.warning("*** THIS CODE SHOULD NOT BE INVOKED DURING **SAVE** Database Object ***")
    # _logger.info("Generate Key: {}".format(inputs))

    sshkeymode = inputs.get('sshkeymode')

    if sshkeymode: # in ['auto', 'user_storage', 'user_ontime']:
        _logger.warning("*** EXTRA CALL - NEED TO BE INVESTIGATED. SKIPPED ***")
        return inputs

    keyKind = inputs.get('keykind', 'rsa')
    pubKey  = inputs.get('publickey', None)
    privKey = inputs.get('privatekey', None)
    keyname = inputs.get('sshkeyname', None)
    username = inputs.get('email_secret', "")

    length = int(inputs.get('keysize', 2048))
    password = inputs.get('passphrase', None)

    private_key = None
    public_key = None
    private_key_obj = None
    extra_public_key = None
    fingerprint = ""

    if is_valid_uuid(keyname):
        private_key, public_key, _kind_, _passphrase_ = load_ssh_from_database(keyname)
        if private_key:
            sshkeymode = "user"
            fingerprint = "PLEAE FIX ME"
        else:
            extra_public_key = public_key
    if privKey and not private_key:
        private_key_obj, private_key = existed_ssh_key_pair(privKey, keyKind, password)
        sshkeymode = "user"
    if not privKey and not private_key:
        private_key_obj, private_key = new_ssh_key_pair(keyKind, length, password)
        sshkeymode = "auto"

    if not public_key:
        public_key = ssh_pubkey_gen(private_key_obj, username=username)

    inputs.update(dict(
        sshkeymode  = sshkeymode,
        privatekey  = private_key,
        publickey   = public_key,
        fingerprint = fingerprint or str(hexlify(private_key_obj.get_fingerprint())),
     ))
    if pubKey:
        inputs['publickey_useroriginal'] = pubKey
    if extra_public_key:
        inputs['publickey_useroriginal'] = extra_public_key

    return inputs


def get_private_key_fingerprint(key):
    line = hexlify(key.get_fingerprint())
    return line


def ssh_key_string_to_obj(text, password=None):
    key = None
    try:
        key = paramiko.RSAKey.from_private_key(StringIO(text), password=password)
    except paramiko.SSHException:
        pass

    try:
        key = paramiko.DSSKey.from_private_key(StringIO(text), password=password)
    except paramiko.SSHException:
        pass
    return key


def ssh_pubkey_gen(private_key, username=''):
    if isinstance(private_key, str):
        private_key = ssh_key_string_to_obj(private_key)

    if not isinstance(private_key, (paramiko.RSAKey, paramiko.DSSKey)):
        raise Exception('Invalid private key type')

    username = " " + username if username else ""
    return "{} {}{}".format(private_key.get_name(), private_key.get_base64(), username)


def flush_sshkey(private_data_dir: str,
                 privatekey: str = None,
                 publickey: str = None,
                 cloud: bool = True) -> dict:
    """
    Creates temporary files containing the private data.
    Result:
    {
        'ssh_key': "PUBLICK KEY PATH",
        'ssh_priv': "PUBLICK KEY PATH",
        'ssh_pub': "PUBLIC KEY ITSELF"
    }
    """

    from core.utils.common import get_ssh_version

    sshkey_files = {}

    if not privatekey is None:
        ssh_ver = get_ssh_version()
        ssh_too_old = True    if ssh_ver == "unknown" else Version(ssh_ver) < Version("6.0")
        openssh_keys_supported = ssh_ver != "unknown" and Version(ssh_ver) >= Version("6.5")

        # Bail out now if a private key was provided in OpenSSH format
        # and we're running an earlier version (<6.5).
        if 'OPENSSH PRIVATE KEY' in privatekey and not openssh_keys_supported:
            raise Exception(OPENSSH_KEY_ERROR)

        # OpenSSH formatted keys must have a trailing newline to be
        # accepted by ssh-add.
        if 'OPENSSH PRIVATE KEY' in privatekey and not privatekey.endswith('\n'):
            privatekey += '\n'

        # For credentials used with ssh-add, write to a named pipe which
        # will be read then closed, instead of leaving the SSH key on disk.

        if not cloud and not ssh_too_old:
            try:
                os.mkdir(os.path.join(private_data_dir, 'env'))
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
            path = os.path.join(private_data_dir, 'env', 'ssh_key')
            # ansible_runner.utils.open_fifo_write(path, privatekey.encode())
            sshkey_files['ssh'] = path

        # Ansyble network modules do not yet support ssh-agent.
        # Instead, ssh private key file is explicitly passed via an
        # env variable.
        else:
            handle, path = tempfile.mkstemp(dir=private_data_dir)
            f = os.fdopen(handle, 'w')
            f.write(privatekey)
            f.close()
            os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
        sshkey_files['ssh_key'] = path
        sshkey_files['ssh_pub'] = publickey

        # --

        handle, path = tempfile.mkstemp(dir=private_data_dir)
        f = os.fdopen(handle, 'w')
        f.write(privatekey)
        f.close()
        os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)

        sshkey_files['ssh_priv'] = path

        _logger.info("ssh key write path:  {}".format(path))

    return sshkey_files


def load_privatekey_from_db(uuid):
    from core.models import UserSecret
    secret = UserSecret.objects.filter(uuid=uuid).first()
    return secret.inputs if secret else None


def sshkey_sotre_to_filesystem(instance, private_data_dir):

    inputs = instance.get('inputs', {})
    cloud = instance.get('cloud')

    privatekey = inputs.get('privatekey', None)
    publickey  = inputs.get('publickey', None)

    files = flush_sshkey(private_data_dir, privatekey, publickey, cloud)
    result = dict(credentials=files)

    return result


def get_or_build_sshkey(*args, **kwargs):
    """ BACKWARD COMPATIBILITY - REMOVE THIS METHOD """
    return sshkey_sotre_to_filesystem(*args, **kwargs)