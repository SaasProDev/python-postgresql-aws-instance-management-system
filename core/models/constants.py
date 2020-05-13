# todo Review & merge to core.constants file

from django.utils.translation import ugettext_lazy as _

CLOUD_LISTS = ['ec2', 'amazon_ec2', 'ms_azure', 'azure_rm', 'google_ce', 'gce']

ORGANISATION_MODEL = 'account.Organization'

ACTION_CHOICES = [
    ('start', _('Start')),              # start, run, create, or configure asset.
    ('stop', _('Stop')),                # stop, poweroff asset.
    ('check', _('Check')),              # synchronize/check asset.
    ('deploy', _('Deploy')),            # deployment asset.
    ('reconfigure', _('Reconfigure')),  # remove and create asset.
    ('remove', _('Remove')),            # remove the asset.
]


DEFAULT_CREDENTIAL_SCHEMA = [{
        "name": "inventory",
        "label": "Hostname or IP",
        "type": "text",
        "required": 1,
        "help_text": "Enter remote IP or Hostname"
    },
    {
        "name": "username",
        "label": "Username",
        "type": "text",
        "required": 1,
        "help_text": "Enter your Username"
    },

    {
        "name": "password",
        "label": "Password",
        "type": "password",
        "required": 1,
        "help_text": "Enter your SSH Password"
    }
 ]
