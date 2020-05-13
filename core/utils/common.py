import json
import yaml

import re
import subprocess

import urllib.parse

import yaql
import os

from functools import reduce, wraps


from logging import getLogger

# Django
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

from rest_framework.exceptions import ParseError
from django.utils.encoding import smart_str
from django.utils.text import slugify
from django.apps import apps


from django.db.models import ForeignKey

_logger = getLogger(__name__)

from .memoize import memoize, memoize_delete, get_memoize_cache

from .sshkeys_utils import (generate_inputs_sshkeys,
                            get_private_key_fingerprint,
                            ssh_key_string_to_obj,
                            get_ssh_version,
                            ssh_pubkey_gen) # noqa


def is_valid_uuid(uuid_to_test):
    UUID_PATTERN = re.compile(r'^[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}$', re.IGNORECASE)
    try:
        return UUID_PATTERN.match(uuid_to_test)
    except:
        return False


def get_fk_model(model, fieldname):
    '''returns None if not foreignkey, otherswise the relevant model'''
    field_object, model, direct, m2m = model._meta.get_field_by_name(fieldname)
    if not m2m and direct and isinstance(field_object, ForeignKey):
        return field_object.rel.to
    return None


def get_model_from_str(model):
    """
    return model from the name
    """

    # obj = model_name
    
    try:
        app_label, model_name = model.split(".")
    except Exception as e:
        app_label = 'core'
        model_name = model
        
    obj = apps.get_model(app_label=app_label, model_name=model_name)

    return obj #instance._meta.model


def get_object_or_400(klass, *args, **kwargs):
    '''
    Return a single object from the given model or queryset based on the query
    params, otherwise raise an exception that will return in a 400 response.
    '''
    from django.shortcuts import _get_queryset
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist as e:
        raise ParseError(*e.args)
    except queryset.model.MultipleObjectsReturned as e:
        raise ParseError(*e.args)


def to_python_boolean(value, allow_none=False):
    value = str(value)
    if value.lower() in ('true', '1', 't'):
        return True
    elif value.lower() in ('false', '0', 'f'):
        return False
    elif allow_none and value.lower() in ('none', 'null'):
        return None
    else:
        raise ValueError(_(u'Unable to convert "%s" to boolean') % value)


def region_sorting(region):
    # python3's removal of sorted(cmp=...) is _stupid_
    if region[1].lower() == 'all':
        return ''
    elif region[1].lower().startswith('us'):
        return region[1]
    return 'ZZZ' + str(region[1])


def camelcase_to_underscore(s):
    '''
    Convert CamelCase names to lowercase_with_underscore.
    '''
    s = re.sub(r'(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))', '_\\1', s)
    return s.lower().strip('_')


def underscore_to_camelcase(s):
    '''
    Convert lowercase_with_underscore names to CamelCase.
    '''
    return ''.join(x.capitalize() or '_' for x in s.split('_'))




def _get_ansible_version(ansible_path):
    '''
    Return Ansible version installed.
    Ansible path needs to be provided to account for custom virtual environments
    '''
    try:
        proc = subprocess.Popen([ansible_path, '--version'],
                                stdout=subprocess.PIPE)
        result = smart_str(proc.communicate()[0])
        return result.split('\n')[0].replace('ansible', '').strip()
    except Exception:
        return 'unknown'


@memoize()
def get_ansible_version():
    return _get_ansible_version('ansible')


def update_scm_url(scm_type, url, username=True, password=True,
                   check_special_cases=True, scp_format=False):
    '''
    Update the given SCM URL to add/replace/remove the username/password. When
    username/password is True, preserve existing username/password, when
    False (None, '', etc.), remove any existing username/password, otherwise
    replace username/password. Also validates the given URL.
    '''
    # Handle all of the URL formats supported by the SCM systems:
    # git: https://www.kernel.org/pub/software/scm/git/docs/git-clone.html#URLS
    # hg: http://www.selenic.com/mercurial/hg.1.html#url-paths
    # svn: http://svnbook.red-bean.com/en/1.7/svn-book.html#svn.advanced.reposurls
    if scm_type not in ('git', 'hg', 'svn', 'insights'):
        raise ValueError(_('Unsupported SCM type "%s"') % str(scm_type))
    if not url.strip():
        return ''
    parts = urllib.parse.urlsplit(url)
    try:
        parts.port
    except ValueError:
        raise ValueError(_('Invalid %s URL') % scm_type)
    if parts.scheme == 'git+ssh' and not scp_format:
        raise ValueError(_('Unsupported %s URL') % scm_type)

    if '://' not in url:
        # Handle SCP-style URLs for git (e.g. [user@]host.xz:path/to/repo.git/).
        if scm_type == 'git' and ':' in url:
            if '@' in url:
                userpass, hostpath = url.split('@', 1)
            else:
                userpass, hostpath = '', url
            if hostpath.count(':') > 1:
                raise ValueError(_('Invalid %s URL') % scm_type)
            host, path = hostpath.split(':', 1)
            #if not path.startswith('/') and not path.startswith('~/'):
            #    path = '~/%s' % path
            #if path.startswith('/'):
            #    path = path.lstrip('/')
            hostpath = '/'.join([host, path])
            modified_url = '@'.join(filter(None, [userpass, hostpath]))
            # git+ssh scheme identifies URLs that should be converted back to
            # SCP style before passed to git module.
            parts = urllib.parse.urlsplit('git+ssh://%s' % modified_url)
        # Handle local paths specified without file scheme (e.g. /path/to/foo).
        # Only supported by git and hg.
        elif scm_type in ('git', 'hg'):
            if not url.startswith('/'):
                parts = urllib.parse.urlsplit('file:///%s' % url)
            else:
                parts = urllib.parse.urlsplit('file://%s' % url)
        else:
            raise ValueError(_('Invalid %s URL') % scm_type)

    # Validate that scheme is valid for given scm_type.
    scm_type_schemes = {
        'git': ('ssh', 'git', 'git+ssh', 'http', 'https', 'ftp', 'ftps', 'file'),
        'hg': ('http', 'https', 'ssh', 'file'),
        'svn': ('http', 'https', 'svn', 'svn+ssh', 'file'),
        'insights': ('http', 'https')
    }
    if parts.scheme not in scm_type_schemes.get(scm_type, ()):
        raise ValueError(_('Unsupported %s URL') % scm_type)
    if parts.scheme == 'file' and parts.netloc not in ('', 'localhost'):
        raise ValueError(_('Unsupported host "%s" for file:// URL') % (parts.netloc))
    elif parts.scheme != 'file' and not parts.netloc:
        raise ValueError(_('Host is required for %s URL') % parts.scheme)
    if username is True:
        netloc_username = parts.username or ''
    elif username:
        netloc_username = username
    else:
        netloc_username = ''
    if password is True:
        netloc_password = parts.password or ''
    elif password:
        netloc_password = password
    else:
        netloc_password = ''

    # Special handling for github/bitbucket SSH URLs.
    if check_special_cases:
        special_git_hosts = ('github.com', 'bitbucket.org', 'altssh.bitbucket.org')
        if scm_type == 'git' and parts.scheme.endswith('ssh') and parts.hostname in special_git_hosts and netloc_username != 'git':
            raise ValueError(_('Username must be "git" for SSH access to %s.') % parts.hostname)
        if scm_type == 'git' and parts.scheme.endswith('ssh') and parts.hostname in special_git_hosts and netloc_password:
            #raise ValueError('Password not allowed for SSH access to %s.' % parts.hostname)
            netloc_password = ''
        special_hg_hosts = ('bitbucket.org', 'altssh.bitbucket.org')
        if scm_type == 'hg' and parts.scheme == 'ssh' and parts.hostname in special_hg_hosts and netloc_username != 'hg':
            raise ValueError(_('Username must be "hg" for SSH access to %s.') % parts.hostname)
        if scm_type == 'hg' and parts.scheme == 'ssh' and netloc_password:
            #raise ValueError('Password not supported for SSH with Mercurial.')
            netloc_password = ''

    if netloc_username and parts.scheme != 'file' and scm_type != "insights":
        netloc = u':'.join([urllib.parse.quote(x,safe='') for x in (netloc_username, netloc_password) if x])
    else:
        netloc = u''
    netloc = u'@'.join(filter(None, [netloc, parts.hostname]))
    if parts.port:
        netloc = u':'.join([netloc, str(parts.port)])
    new_url = urllib.parse.urlunsplit([parts.scheme, netloc, parts.path,
                                       parts.query, parts.fragment])
    if scp_format and parts.scheme == 'git+ssh':
        new_url = new_url.replace('git+ssh://', '', 1).replace('/', ':', 1)
    return new_url


def get_type_for_model(model):
    '''
    Return type name for a given model class.
    '''
    opts = model._meta.concrete_model._meta
    return camelcase_to_underscore(opts.object_name)

def get_model_for_type(type_name):
    '''
    Return model class for a given type name.
    '''
    model_str = underscore_to_camelcase(type_name)
    if model_str == 'User':
        use_app = 'auth'
    else:
        use_app = 'core'
    return apps.get_model(use_app, model_str)



def validate_vars_type(vars_obj):
    if not isinstance(vars_obj, dict):
        vars_type = type(vars_obj)
        if hasattr(vars_type, '__name__'):
            data_type = vars_type.__name__
        else:
            data_type = str(vars_type)
        raise AssertionError(
            _('Input type `{data_type}` is not a dictionary').format(
                data_type=data_type)
        )


def parse_yaml_or_json(vars_str, silent_failure=True):
    '''
    Attempt to parse a string of variables.
    First, with JSON parser, if that fails, then with PyYAML.
    If both attempts fail, return an empty dictionary if `silent_failure`
    is True, re-raise combination error if `silent_failure` if False.
    '''
    if isinstance(vars_str, dict):
        return vars_str
    elif isinstance(vars_str, str) and vars_str == '""':
        return {}

    try:
        vars_dict = json.loads(vars_str)
        validate_vars_type(vars_dict)
    except (ValueError, TypeError, AssertionError) as json_err:
        try:
            vars_dict = yaml.safe_load(vars_str)
            # Can be None if '---'
            if vars_dict is None:
                vars_dict = {}
            validate_vars_type(vars_dict)
            if not silent_failure:
                # is valid YAML, check that it is compatible with JSON
                try:
                    json.dumps(vars_dict)
                except (ValueError, TypeError, AssertionError) as json_err2:
                    raise ParseError(_(
                        'Variables not compatible with JSON standard (error: {json_error})').format(
                            json_error=str(json_err2)))
        except (yaml.YAMLError, TypeError, AttributeError, AssertionError) as yaml_err:
            if silent_failure:
                return {}
            raise ParseError(_(
                'Cannot parse as JSON (error: {json_error}) or '
                'YAML (error: {yaml_error}).').format(
                    json_error=str(json_err), yaml_error=str(yaml_err)))
    return vars_dict



def get_pk_from_dict(_dict, key):
    '''
    Helper for obtaining a pk from user data dict or None if not present.
    '''
    try:
        val = _dict[key]
        if isinstance(val, object) and hasattr(val, 'id'):
            return val.id  # return id if given model object
        return int(val)
    except (TypeError, KeyError, ValueError):
        return None


class NoDefaultProvided(object):
    pass


def getattrd(obj, name, default=NoDefaultProvided):
    """
    Same as getattr(), but allows dot notation lookup
    Discussed in:
    http://stackoverflow.com/questions/11975781
    """

    try:
        return reduce(getattr, name.split("."), obj)
    except AttributeError:
        if default != NoDefaultProvided:
            return default
        raise


def getattr_dne(obj, name, notfound=ObjectDoesNotExist):
    try:
        return getattr(obj, name)
    except notfound:
        return None


current_apps = apps


def set_current_apps(apps):
    global current_apps
    current_apps = apps


def get_current_apps():
    global current_apps
    return current_apps


def is_ansible_variable(key):
    return key.startswith('ansible_')


def extract_ansible_vars(extra_vars):
    extra_vars = parse_yaml_or_json(extra_vars)
    ansible_vars = set([])
    for key in list(extra_vars.keys()):
        if is_ansible_variable(key):
            extra_vars.pop(key)
            ansible_vars.add(key)
    return (extra_vars, ansible_vars)


def get_search_fields(model):
    fields = []
    for field in model._meta.fields:
        if field.name in ('username', 'first_name', 'last_name', 'email',
                          'name', 'description'):
            fields.append(field.name)
    return fields


def to_slugify(text):
    from slugify import slugify, Slugify, UniqueSlugify
    c__slugify = Slugify(to_lower=True)
    c__slugify.separator = '_'

    return c__slugify( text )


def load_yml_to_dict(path, k = None):

    map__data = dict()
    
    try:
        map__data = yaml.load(open(path), Loader=yaml.SafeLoader)

        if map__data:
            if k:
                if map__data.get(k):
                    return map__data.get(k)

        return dict()

    except Exception as e:
        raise e

    return dict()



def ahomefile_to_dict(namespace):

    map__data = dict()
    try:
        
        ahomefile = "{}/{}/index.yml".format(settings.AHOME_LOCAL_ANSIBLE_ROLES_PATH, namespace)
        if not os.path.isfile(ahomefile):
            ahomefile = "{}/{}.yml".format(settings.AHOMEMAPPINGS_PATH, namespace)

        map__data = yaml.load(open(ahomefile), Loader=yaml.SafeLoader)
        
    except Exception as e:
        # raise e
        _logger.warning("{} - file does not exist error: {}".format("utils/common.py - ahomefile_to_dict", e))
        return dict()

    return map__data



def dict_yaql(data, query):
    try:

        # data_source = json.loads('{"customers_city": [{"city": "New York", "customer_id": 1}, {"city": "Saint Louis", "customer_id": 2}, {"city": "Mountain View", "customer_id": 3}], "customers": [{"customer_id": 1, "name": "John", "orders": [{"order_id": 1, "item": "Guitar", "quantity": 1}]}, {"customer_id": 2, "name": "Paul", "orders": [{"order_id": 2, "item": "Banjo", "quantity": 2}, {"order_id": 3, "item": "Piano", "quantity": 1}]}, {"customer_id": 3, "name": "Diana", "orders": [{"order_id": 4, "item": "Drums", "quantity": 1}]}]}')
        # sdata = json.loads(data)

        engine = yaql.factory.YaqlFactory().create()

        # query = '$.customers.orders.selectMany($.where($.order_id = 4)).where($.item = Drums).select($.item)'

        expression = engine( query )
        order = expression.evaluate(data=data)
        return order
    except KeyError as e:
        _logger.warning("{} - error: {}".format("utils/common.py - dict_yaql", e))
    except Exception as e:
        _logger.warning("{}: query: {} => data: {}".format("utils/common.py - dict_yaql", query, data))
        return []



def ahomefile_yaql(data, qs, out='string'):
    try:

        engine = yaql.factory.YaqlFactory().create()

        query = "$.{}".format(qs)

        expression = engine( query )
        order = expression.evaluate(data=data)
        return order
    except KeyError as e:
        _logger.warning("{} - error: {}".format("utils/common.py - ahomefile_yaql", e))
    except Exception as e:
        _logger.warning("{}: query: {} => data: {}".format("utils/common.py - ahomefile_yaql", query, data))
        return []




def append_ahomefile_fields(src, field):

    engine = yaql.factory.YaqlFactory().create()

    query = '$.where($.fieldRef = "{}").len()'.format( field.get("fieldRef") )

    expression = engine( query )
    q_count = expression.evaluate(data=src)
    # print (q_count)

    if q_count == 0:
        src.append(field)
        return src
    else:
        query = '$.where($.fieldRef = "{}").first()'.format( field.get("fieldRef") )
        expression = engine( query )
        q_result = expression.evaluate(data=src)
        
        a = q_result.get("value")
        if isinstance(a, dict):
            a.update({ field.get("name"): field.get("value") })
        else:
            a = { q_result.get("name"): q_result.get("value"), field.get("name"): field.get("value") }

        q_result.update({ "value": a })
        # print (q_result)

        query = '$.where($.fieldRef != "{}")'.format( field.get("fieldRef") )
        expression = engine( query )
        f_result = expression.evaluate(data=src)

        f_result.append(q_result)

        return f_result

