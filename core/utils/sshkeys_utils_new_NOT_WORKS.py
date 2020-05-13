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


##AHOME_SSKEYROOT_BASE_PATH



# TODO : change the path to a secure workspace
def generate_inputs_sshkeys(inputs):
    # _logger.info("Generate Key: {}".format(inputs))

    f = io.StringIO()

    username = 'admin'

    hostname = os.uname()[1]

    if inputs.get('keykind'):
        if not inputs.get('publickey') or not inputs.get('privatekey'):

            length = int(inputs.get('keysize', 2048))
            password = inputs.get('passphrase', None)

            # _logger.info(f"length: {length} - password: {password}")

            try:
                if inputs.get('keykind') == 'rsa':
                    private_key_obj = paramiko.RSAKey.generate(length)
                elif inputs.get('keykind') == 'dsa':
                    private_key_obj = paramiko.DSSKey.generate(length)
                else:
                    raise IOError('SSH private key must be `rsa` or `dsa`')
                if password:
                    private_key_obj.write_private_key(f, password=password)
                else:
                    private_key_obj.write_private_key(f, password=None)
                private_key = f.getvalue()
                public_key = ssh_pubkey_gen(private_key_obj, username=username, hostname=hostname)
                fingerprint = str(hexlify(
                    private_key_obj.get_fingerprint()))  # get_private_key_fingerprint(private_key_obj) #hexlify(private_key_obj.get_fingerprint())

                # _logger.info(f"**** fingerprint: {fingerprint}")

                inputs.update(dict(
                    privatekey=private_key,
                    publickey=public_key,
                    fingerprint=fingerprint,
                ))

            except IOError:
                raise IOError('These is error when generate ssh key.')

        # if not inputs.get('privatekey'):

        #     key = RSA.generate(2048)

        #     with open("/tmp/mykey.pem", "wb") as f:
        #         f.write( key.export_key('PEM') )

        #     f = open('/tmp/mykey.pem','r')
        #     inputs.update( dict (privatekey = f.read() ))

        # if not inputs.get('publickey'):

        #     with open("/tmp/mykey.pem", "w") as f:
        #         f.write( inputs.get('privatekey') )

        #     f = open('/tmp/mykey.pem','r')
        #     key = RSA.import_key(f.read())

        #     with open("/tmp/mypubkey.pem", "wb") as f:
        #         f.write( key.publickey().export_key('OpenSSH') )

        #     f = open('/tmp/mypubkey.pem','r')
        #     inputs.update( dict (publickey = f.read() ))

        # if not inputs.get('fingerprint'):

        #     with open("/tmp/mykey.pem", "w") as f:
        #         f.write( inputs.get('privatekey') )

        #     k = paramiko.RSAKey.from_private_key_file("/tmp/mykey.pem")
        #     inputs.update( dict(fingerprint = hexlify(k.get_fingerprint()) ) )

    # if not inputs.get('publickey'):

    #     if not inputs.get('privatekey'):

    #         key = RSA.generate(2048)

    #         f = open('/tmp/mykey.pem','wb')
    #         f.write(key.export_key('PEM'))
    #         f.close()

    #         f = open('/tmp/mykey.pem','r')
    #         inputs.update( dict (privatekey = f.read() ))

    #         f = open('/tmp/mypubkey.pem','wb')
    #         f.write( key.publickey().export_key('OpenSSH') )
    #         f.close()

    #         f = open('/tmp/mypubkey.pem','r')
    #         inputs.update( dict(publickey = f.read()) )

    #         k = paramiko.RSAKey.from_private_key_file("/tmp/mykey.pem")
    #         inputs.update( dict(fingerprint = hexlify(k.get_fingerprint()) ) )

    #     else:
    #         # f = io.StringIO(str.encode(instance.privatekey))
    #         with open("/tmp/mykey1.pem", "w") as f:
    #             f.write( inputs.get('privatekey') )

    #         f = open('/tmp/mykey1.pem','r')
    #         key = RSA.import_key(f.read())

    #         f = open('/tmp/mypubkey.pem','wb')
    #         f.write( key.publickey().export_key('OpenSSH') )
    #         f.close()

    #         f = open('/tmp/mypubkey.pem','r')

    #         k = paramiko.RSAKey.from_private_key_file("/tmp/mykey1.pem")

    #         inputs.update( dict(fingerprint = hexlify(k.get_fingerprint()) ) )

    #     inputs.update( dict(publickey = f.read()) )

    # _logger.info("** Inputs: {}".format(inputs))

    return inputs


def get_private_key_fingerprint(key):
    line = hexlify(key.get_fingerprint())
    return line
    # return b':'.join([line[i:i+2] for i in range(0, len(line), 2)])


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


def ssh_pubkey_gen(private_key=None, username='jumpserver', hostname='localhost'):
    if isinstance(private_key, str):
        private_key = ssh_key_string_to_obj(private_key)

    if not isinstance(private_key, (paramiko.RSAKey, paramiko.DSSKey)):
        raise IOError('Invalid private key')

    # public_key = "%(key_type)s %(key_content)s %(username)s@%(hostname)s" % {
    #     'key_type': private_key.get_name(),
    #     'key_content': private_key.get_base64(),
    #     'username': username,
    #     'hostname': hostname,
    # }

    public_key = "%(key_type)s %(key_content)s" % {
        'key_type': private_key.get_name(),
        'key_content': private_key.get_base64(),
    }

    return public_key


def ssh_key_gen(length=2048, type='rsa', password=None, username='jumpserver', hostname=None):
    """Generate user ssh private and public key
    Use paramiko RSAKey generate it.
    :return private key str and public key str
    """

    if hostname is None:
        hostname = os.uname()[1]

    f = StringIO()

    try:
        if type == 'rsa':
            private_key_obj = paramiko.RSAKey.generate(length)
        elif type == 'dsa':
            private_key_obj = paramiko.DSSKey.generate(length)
        else:
            raise IOError('SSH private key must be `rsa` or `dsa`')
        private_key_obj.write_private_key(f, password=password)
        private_key = f.getvalue()
        public_key = ssh_pubkey_gen(private_key_obj, username=username, hostname=hostname)
        return private_key, public_key
    except IOError:
        raise IOError('These is error when generate ssh key.')


OPENSSH_KEY_ERROR = u'''\
It looks like you're trying to use a private key in OpenSSH format, which \
isn't supported by the installed version of OpenSSH on this instance. \
Try upgrading OpenSSH or providing your private key in an different format. \
'''


def get_or_build_sshkey(instance, private_data_dir, iaas_inputs=None):
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

    from .common import get_ssh_version

    iaas_inputs = iaas_inputs or {}

    kind    = instance.get('kind')
    inputs  = instance.get('inputs', {})
    cloud   = instance.get('cloud')

    sshkey_files = dict(credentials=dict())

    key_source = inputs if inputs.get('privatekey') else iaas_inputs
    sshkey = dict(
        privatekey=key_source.get('privatekey', None),
        publickey=key_source.get('publickey', None)
    )

    if sshkey.get('privatekey') is not None:
        data = sshkey.get('privatekey')

        ssh_ver = get_ssh_version()
        ssh_too_old    = True if ssh_ver == "unknown" else Version(ssh_ver) <  Version("6.0")
        openssh_keys_supported = ssh_ver != "unknown" and  Version(ssh_ver) >= Version("6.5")

        # Bail out now if a private key was provided in OpenSSH format
        # and we're running an earlier version (<6.5).
        if 'OPENSSH PRIVATE KEY' in data and not openssh_keys_supported:
            raise Exception(OPENSSH_KEY_ERROR)

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
                    raise Exception("Cannot create folder '{}' "
                                    "for SSH keys. errno: {} ".format(private_data_dir, e.errno))
            path = os.path.join(private_data_dir, 'env', 'ssh_key')

            _logger.warning("**** SSH for NOT CLOUD DOES NOT IMPLEMENTED HERE *** ")
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

        sshkey_files['credentials']['ssh_priv'] = path
        sshkey_files['credentials']['ssh_key'] = path
        sshkey_files['credentials']['ssh_pub'] = sshkey.get('publickey')

        # handle, path = tempfile.mkstemp(dir=private_data_dir)
        # f = os.fdopen(handle, 'w')
        # f.write(data)
        # f.close()
        # os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
        #
        # sshkey_files['credentials']['ssh_priv'] = path
        #
        # _logger.info("ssh key write path:  {}".format(path))

    return sshkey_files