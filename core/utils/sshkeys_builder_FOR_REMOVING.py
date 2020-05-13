"""
todo Please merge all SSH Based routines into a single one
This is (an updated) copy from 'core.tasks.base_task' module
"""
import os
import errno
import stat
import tempfile
# import piramiko
from core.utils.common import get_ssh_version
from distutils.version import LooseVersion as Version

from logging import getLogger

_logger = getLogger(__name__)

OPENSSH_KEY_ERROR = u'''\
It looks like you're trying to use a private key in OpenSSH format, which \
isn't supported by the installed version of OpenSSH on this instance. \
Try upgrading OpenSSH or providing your private key in an different format. \
'''

# todo REMOVE THIS
def ORIGINAL_build__sshkey(instance, private_data_dir):
    """
    Creates temporary files containing the private data.
    Returns a dictionary i.e.,
    {
        'sshkeys': {
            'privatekey': '/path/to/decrypted/private_data',
            'publickey': '/path/to/decrypted/public_data',
            ...
        }
    }
    """

    kind = instance.get('kind')
    inputs = instance.get('inputs', {})
    cloud = instance.get('cloud')

    sshkey_files = dict(credentials=dict())

    sshkey = dict(
        privatekey=inputs.get('privatekey', None),
        publickey=inputs.get('publickey', None)
    )

    if not sshkey.get('privatekey') is None:
        ssh_ver = get_ssh_version()
        ssh_too_old = True if ssh_ver == "unknown" else Version(ssh_ver) < Version("6.0")
        openssh_keys_supported = ssh_ver != "unknown" and Version(ssh_ver) >= Version("6.5")

        data = sshkey.get('privatekey')

        # Bail out now if a private key was provided in OpenSSH format
        # and we're running an earlier version (<6.5).
        if 'OPENSSH PRIVATE KEY' in data and not openssh_keys_supported:
            raise RuntimeError(OPENSSH_KEY_ERROR)
        # OpenSSH formatted keys must have a trailing newline to be
        # accepted by ssh-add.
        if 'OPENSSH PRIVATE KEY' in data and not data.endswith('\n'):
            data += '\n'
        # For credentials used with ssh-add, write to a named pipe which
        # will be read then closed, instead of leaving the SSH key on disk.

        if not cloud and not ssh_too_old:
            try:
                os.mkdir(os.path.join(private_data_dir, 'env'))
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
            path = os.path.join(private_data_dir, 'env', 'ssh_key')
            # ansible_runner.utils.open_fifo_write(path, data.encode())
            sshkey_files['credentials']['ssh'] = path

        # Ansible network modules do not yet support ssh-agent.
        # Instead, ssh private key file is explicitly passed via an
        # env variable.
        else:
            handle, path = tempfile.mkstemp(dir=private_data_dir)
            f = os.fdopen(handle, 'w')
            f.write(data)
            f.close()
            os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
        sshkey_files['credentials']['ssh_key'] = path
        sshkey_files['credentials']['ssh_pub'] = sshkey.get('publickey')

        # --

        handle, path = tempfile.mkstemp(dir=private_data_dir)
        f = os.fdopen(handle, 'w')
        f.write(data)
        f.close()
        os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)

        sshkey_files['credentials']['ssh_priv'] = path

        _logger.info("ssh key write path:  {}".format(path))

    return sshkey_files


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

    sshkey_files  = {}

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


def build__sshkey(instance, private_data_dir):
    from pprint import pformat
    # from piramiko

    inputs = instance.get('inputs', {})
    cloud = instance.get('cloud')

    privatekey = inputs.get('privatekey', None)
    publickey  = inputs.get('publickey', None)
    sshkeyname = inputs.get('sshkeyname', None)

    _logger.warning("**** ATTENTION *** SECURITY ISSUE - MUST BE REMOVED ****")
    _logger.warning("**** ATTENTION *** SECURITY ISSUE - MUST BE REMOVED ****")
    _logger.warning("**** ATTENTION *** SECURITY ISSUE - MUST BE REMOVED ****")

    _logger.warning("privatekey: [{}]".format(privatekey))
    _logger.warning("publickey:  [{}]".format(publickey))
    _logger.warning("sshkeyname: [{}]".format(sshkeyname))

    if privatekey is None and sshkeyname is not None:
        _logger.debug("UserCredential uuid: [{}]".format(sshkeyname))
        secret = load_privatekey_from_db(sshkeyname)
        if 'publickey'  in secret:
            publickey = secret['publickey']
        else:
            raise Exception("NO SSH Key defined for UserCredential '{}'".format(sshkeyname))

    files = flush_sshkey(private_data_dir, privatekey, publickey, cloud)
    result = dict(credentials=files)

    from pprint import pformat

    _logger.debug(pformat(result, indent=4))

    return result
