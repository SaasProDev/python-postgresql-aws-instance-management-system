from django.db import models
from django.conf import settings as django_settings

from .constants import *
from .fields import IPNetworkField, IPAddressField

from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.expressions import RawSQL
from django.utils.translation import ugettext_lazy as _

from django.utils.encoding import smart_str
from django.utils.timezone import now

from django.contrib.postgres.fields import HStoreField
from django.contrib.postgres.fields import ArrayField

# from django.urls import reverse
from rest_framework.reverse import reverse
# from django.urls import reverse

import xmltodict, json

import netaddr
import uuid
import time
from datetime import datetime
# jsonschema
from jsonschema import Draft4Validator, FormatChecker
import jsonschema.exceptions

#from django.contrib.auth.models import Permission, User, Group
from django.contrib.auth.models import Permission

from core.utils import get_model_from_str, load_yml_to_dict, ahomefile_to_dict, dict_yaql, append_ahomefile_fields, ahomefile_yaql, get_ssh_version, generate_inputs_sshkeys

# Django-JSONField
from django.contrib.postgres.fields import JSONField
# from jsonfield import JSONField as upstream_JSONField

#from awx.main.utils import parse_yaml_or_json, getattr_dne
#from awx.main.fields import ImplicitRoleField, JSONField, AskForField


#from django.conf import settings

from account.models import Organization
#TODO
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

STATUS_CHOICES = django_settings.STATUS_CHOICES

"""
XSTATUS_CHOICES = [
    ('new', _('New')),                  # Job has been created, but not started.
    ('pending', _('Pending')),          # Job is pending Task Manager processing (blocked by dependency req, capacity or a concurrent job)
    ('waiting', _('Waiting')),          # Job has been assigned to run on a specific node (and is about to run).
    ('starting', _('Starting')),        # Job is starting.
    ('running', _('Running')),          # Job is currently running.
    ('successful', _('Successful')),    # Job completed successfully.
    ('failed', _('Failed')),            # Job completed, but with failures.
    ('error', _('Error')),              # The job was unable to run.
    ('canceled', _('Canceled')),        # The job was canceled before completion.
]
"""

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






def jsonfield_default():
    return dict()

def generic_schema():
    return json.dumps(DEFAULT_CREDENTIAL_SCHEMA)



class CreatedUpdatedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    # is_obselete = models.BooleanField(default=False)

    class Meta:
        abstract = True



class Tag(models.Model):
    name = models.CharField(max_length=60, blank=False, null=False, unique=True)
    font_awesome = models.CharField(max_length=60, blank=False)
 
    objects = models.Manager()
 
    def __str__(self):
        return self.name




class Rir(CreatedUpdatedModel):
    """
    RIR
    """ 
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True, null=True)
    registry = models.CharField(max_length=200, blank=True, null=True, verbose_name='Internet Registry')
    region = models.CharField(max_length=200, blank=True, null=True)
    organization = models.ForeignKey(
        ORGANISATION_MODEL,
        related_name='rirs', 
        on_delete=models.PROTECT, 
        blank=True, 
        null=True
    )
    hosted = models.CharField(max_length=200, null=True , blank=True)
    definition = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )
    kind = models.CharField(max_length=200, blank=True, default='rir')


    class Meta:
        ordering = ['name']
        verbose_name = 'RIR'
        verbose_name_plural = 'RIRs'


    def __str__(self):
        return self.name



class Vrf(CreatedUpdatedModel):
    """
    A virtual routing and forwarding (VRF) table represents a discrete layer three forwarding domain (e.g. a routing
    table). Prefixes and IPAddresses can optionally be assigned to VRFs. (Prefixes and IPAddresses not assigned to a VRF
    are said to exist in the "global" table.)
    """
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True, null=True)
    rd = models.CharField(max_length=21, verbose_name='Route distinguisher')
    enforce_unique = models.BooleanField(default=True, verbose_name='Enforce unique space',
                                         help_text="Prevent duplicate prefixes/IP addresses within this VRF")
    organization = models.ForeignKey(
        ORGANISATION_MODEL,
        related_name='vrfs', 
        on_delete=models.PROTECT, 
        blank=True, 
        null=True
    )
    hosted = models.CharField(max_length=200, null=True , blank=True)
    definition = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )
    kind = models.CharField(max_length=200, blank=True, default='vrf')



    class Meta:
        ordering = ['name']
        verbose_name = 'VRF'
        verbose_name_plural = 'VRFs'

    def __str__(self):
        return self.display_name or super(Vrf, self).__str__()

    @property
    def display_name(self):
        if self.name and self.rd:
            return "{} ({})".format(self.name, self.rd)
        return None


class Aggregate(CreatedUpdatedModel):
    """
    An aggregate exists at the root level of the IP address space hierarchy in NetBox. Aggregates are used to organize
    the hierarchy and track the overall utilization of available address space. Each Aggregate is assigned to a RIR.
    """
    family = models.PositiveSmallIntegerField(choices=AF_CHOICES, editable=False)
    prefix = IPNetworkField()
    rir = models.ForeignKey('Rir', related_name='aggregates', on_delete=models.PROTECT, verbose_name='RIR')
    date_added = models.DateField(blank=True, null=True)
    description = models.CharField(max_length=100, blank=True)
    organization = models.ForeignKey(
        ORGANISATION_MODEL,
        related_name='aggregates', 
        on_delete=models.PROTECT, 
        blank=True, 
        null=True
    )
    hosted = models.CharField(max_length=200, null=True , blank=True)
    definition = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )
    kind = models.CharField(max_length=200, blank=True, default='aggregate')


    class Meta:
        ordering = ['family', 'prefix']

    def __str__(self):
        return str(self.prefix)

    def clean(self):

        if self.prefix:

            # Clear host bits from prefix
            self.prefix = self.prefix.cidr

            # Ensure that the aggregate being added is not covered by an existing aggregate
            covering_aggregates = Aggregate.objects.filter(prefix__net_contains_or_equals=str(self.prefix))
            if self.pk:
                covering_aggregates = covering_aggregates.exclude(pk=self.pk)
            if covering_aggregates:
                raise ValidationError({
                    'prefix': "Aggregates cannot overlap. {} is already covered by an existing aggregate ({}).".format(
                        self.prefix, covering_aggregates[0]
                    )
                })

            # Ensure that the aggregate being added does not cover an existing aggregate
            covered_aggregates = Aggregate.objects.filter(prefix__net_contained=str(self.prefix))
            if self.pk:
                covered_aggregates = covered_aggregates.exclude(pk=self.pk)
            if covered_aggregates:
                raise ValidationError({
                    'prefix': "Aggregates cannot overlap. {} covers an existing aggregate ({}).".format(
                        self.prefix, covered_aggregates[0]
                    )
                })

    def save(self, *args, **kwargs):
        if self.prefix:
            # Infer address family from IPNetwork object
            self.family = self.prefix.version
        super(Aggregate, self).save(*args, **kwargs)


    def get_utilization(self):
        """
        Determine the prefix utilization of the aggregate and return it as a percentage.
        """
        queryset = Prefix.objects.filter(prefix__net_contained_or_equal=str(self.prefix))
        child_prefixes = netaddr.IPSet([p.prefix for p in queryset])
        return int(float(child_prefixes.size) / self.prefix.size * 100)




class Prefix(CreatedUpdatedModel):
    """
    A Prefix represents an IPv4 or IPv6 network, including mask length. Prefixes can optionally be assigned to Sites and
    VRFs. A Prefix must be assigned a status and may optionally be assigned a used-define Role. A Prefix can also be
    assigned to a VLAN where appropriate.
    """
    family = models.PositiveSmallIntegerField(choices=AF_CHOICES, editable=False)
    prefix = IPNetworkField(help_text="IPv4 or IPv6 network with mask")
    organization = models.ForeignKey(ORGANISATION_MODEL, related_name='prefixes', on_delete=models.PROTECT, blank=True, null=True)
    vrf = models.ForeignKey('Vrf', related_name='prefixes', on_delete=models.PROTECT, blank=True, null=True,
                            verbose_name='VRF')
    vlan = models.ForeignKey('Vlan', related_name='prefixes', on_delete=models.PROTECT, blank=True, null=True,
                             verbose_name='VLAN')
    status = models.PositiveSmallIntegerField('Status', choices=PREFIX_STATUS_CHOICES, default=PREFIX_STATUS_ACTIVE,
                                              help_text="Operational status of this prefix")
    is_pool = models.BooleanField(verbose_name='Is a pool', default=False,
                                  help_text="All IP addresses within this prefix are considered usable")
    description = models.CharField(max_length=100, blank=True)

    hosted = models.CharField(max_length=200, null=True , blank=True)
    definition = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )
    label = models.CharField(max_length=100, null=True, blank=True)

    connected = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )
    kind = models.CharField(max_length=200, blank=True, default='prefix')



    class Meta:
        ordering = ['vrf', 'family', 'prefix']
        verbose_name_plural = 'prefixes'

    def __str__(self):
        return str(self.prefix)




    def clean(self):

        if self.prefix:

            # Disallow host masks
            if self.prefix.version == 4 and self.prefix.prefixlen == 32:
                raise ValidationError({
                    'prefix': "Cannot create host addresses (/32) as prefixes. Create an IPv4 address instead."
                })
            elif self.prefix.version == 6 and self.prefix.prefixlen == 128:
                raise ValidationError({
                    'prefix': "Cannot create host addresses (/128) as prefixes. Create an IPv6 address instead."
                })

            # Enforce unique IP space (if applicable)
            if (self.vrf is None and django_settings.ENFORCE_GLOBAL_UNIQUE) or (self.vrf and self.vrf.enforce_unique):
                duplicate_prefixes = self.get_duplicates()
                if duplicate_prefixes:
                    raise ValidationError({
                        'prefix': "Duplicate prefix found in {}: {}".format(
                            "VRF {}".format(self.vrf) if self.vrf else "global table",
                            duplicate_prefixes.first(),
                        )
                    })

    def save(self, *args, **kwargs):
        if self.prefix:
            # Clear host bits from prefix
            self.prefix = self.prefix.cidr
            # Infer address family from IPNetwork object
            self.family = self.prefix.version
        super(Prefix, self).save(*args, **kwargs)



    def get_status_class(self):
        return STATUS_CHOICE_CLASSES[self.status]

    def get_duplicates(self):
        return Prefix.objects.filter(vrf=self.vrf, prefix=str(self.prefix)).exclude(pk=self.pk)

    def get_child_prefixes(self):
        """
        Return all Prefixes within this Prefix and VRF.
        """
        return Prefix.objects.filter(prefix__net_contained=str(self.prefix), vrf=self.vrf)

    def get_child_ips(self):
        """
        Return all IPAddresses within this Prefix and VRF.
        """
        return IPAddress.objects.filter(address__net_host_contained=str(self.prefix), vrf=self.vrf)

    def get_available_prefixes(self):
        """
        Return all available Prefixes within this prefix as an IPSet.
        """
        prefix = netaddr.IPSet(self.prefix)
        child_prefixes = netaddr.IPSet([child.prefix for child in self.get_child_prefixes()])
        available_prefixes = prefix - child_prefixes

        return available_prefixes

    def get_available_ips(self):
        """
        Return all available IPs within this prefix as an IPSet.
        """
        prefix = netaddr.IPSet(self.prefix)
        child_ips = netaddr.IPSet([ip.address.ip for ip in self.get_child_ips()])
        available_ips = prefix - child_ips

        # Remove unusable IPs from non-pool prefixes
        if not self.is_pool:
            available_ips -= netaddr.IPSet([
                netaddr.IPAddress(self.prefix.first),
                netaddr.IPAddress(self.prefix.last),
            ])

        return available_ips

    def get_first_available_prefix(self):
        """
        Return the first available child prefix within the prefix (or None).
        """
        available_prefixes = self.get_available_prefixes()
        if not available_prefixes:
            return None
        return available_prefixes.iter_cidrs()[0]

    def get_first_available_ip(self):
        """
        Return the first available IP within the prefix (or None).
        """
        available_ips = self.get_available_ips()
        if not available_ips:
            return None
        return '{}/{}'.format(next(available_ips.__iter__()), self.prefix.prefixlen)

    def get_utilization(self):
        """
        Determine the utilization of the prefix and return it as a percentage. For Prefixes with a status of
        "container", calculate utilization based on child prefixes. For all others, count child IP addresses.
        """
        if self.status == PREFIX_STATUS_CONTAINER:
            queryset = Prefix.objects.filter(prefix__net_contained=str(self.prefix), vrf=self.vrf)
            child_prefixes = netaddr.IPSet([p.prefix for p in queryset])
            return int(float(child_prefixes.size) / self.prefix.size * 100)
        else:
            child_count = self.get_child_ips().count()
            prefix_size = self.prefix.size
            if self.family == 4 and self.prefix.prefixlen < 31 and not self.is_pool:
                prefix_size -= 2
            return int(float(child_count) / prefix_size * 100)



class Vlan(CreatedUpdatedModel):
    """
    A VLAN is a distinct layer two forwarding domain identified by a 12-bit integer (1-4094). Each VLAN must be assigned
    to a Site, however VLAN IDs need not be unique within a Site. A VLAN may optionally be assigned to a VLANGroup,
    within which all VLAN IDs and names but be unique.
    Like Prefixes, each VLAN is assigned an operational status and optionally a user-defined Role. A VLAN can have zero
    or more Prefixes assigned to it.
    """
    organization = models.ForeignKey(ORGANISATION_MODEL, related_name='vlans', on_delete=models.PROTECT, blank=True, null=True)
    vid = models.PositiveSmallIntegerField(verbose_name='ID', validators=[
        MinValueValidator(1),
        MaxValueValidator(4094)
    ])
    name = models.CharField(max_length=64)
    status = models.PositiveSmallIntegerField('Status', choices=VLAN_STATUS_CHOICES, default=1)
    description = models.CharField(max_length=100, blank=True)
    hosted = models.CharField(max_length=200, null=True , blank=True)
    definition = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )
    kind = models.CharField(max_length=200, blank=True, default='vlan')

    class Meta:
        ordering = ['organization', 'vid']
        verbose_name = 'VLAN'
        verbose_name_plural = 'VLANs'

    def __str__(self):
        return self.display_name or super(Vlan, self).__str__()


    @property
    def display_name(self):
        if self.vid and self.name:
            return "{} ({})".format(self.vid, self.name)
        return None

    def get_status_class(self):
        return STATUS_CHOICE_CLASSES[self.status]



class IPAddressManager(models.Manager):

    def get_queryset(self):
        """
        By default, PostgreSQL will order INETs with shorter (larger) prefix lengths ahead of those with longer
        (smaller) masks. This makes no sense when ordering IPs, which should be ordered solely by family and host
        address. We can use HOST() to extract just the host portion of the address (ignoring its mask), but we must
        then re-cast this value to INET() so that records will be ordered properly. We are essentially re-casting each
        IP address as a /32 or /128.
        """
        qs = super(IPAddressManager, self).get_queryset()
        return qs.annotate(host=RawSQL('INET(HOST(core_ipaddress.address))', [])).order_by('family', 'host')



class IPAddress(CreatedUpdatedModel):
    """
    An IPAddress represents an individual IPv4 or IPv6 address and its mask. The mask length should match what is
    configured in the real world. (Typically, only loopback interfaces are configured with /32 or /128 masks.) Like
    Prefixes, IPAddresses can optionally be assigned to a VRF. An IPAddress can optionally be assigned to an Interface.
    Interfaces can have zero or more IPAddresses assigned to them.
    An IPAddress can also optionally point to a NAT inside IP, designating itself as a NAT outside IP. This is useful,
    for example, when mapping public addresses to private addresses. When an Interface has been assigned an IPAddress
    which has a NAT outside IP, that Interface's Device can use either the inside or outside IP as its primary IP.
    """
    organization = models.ForeignKey(ORGANISATION_MODEL, related_name='ip_addresses', on_delete=models.PROTECT, blank=True, null=True)
    family = models.PositiveSmallIntegerField(choices=AF_CHOICES, editable=False)
    address = IPAddressField(help_text="IPv4 or IPv6 address (with mask)")
    vrf = models.ForeignKey('VRF', related_name='ip_addresses', on_delete=models.PROTECT, blank=True, null=True,
                            verbose_name='VRF')
    status = models.PositiveSmallIntegerField(
        'Status', choices=IPADDRESS_STATUS_CHOICES, default=IPADDRESS_STATUS_ACTIVE,
        help_text='The operational status of this IP'
    )

    description = models.CharField(max_length=100, blank=True)

    hosted = models.CharField(max_length=200, null=True , blank=True)
    definition = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )
    label = models.CharField(max_length=100, null=True, blank=True)

    connected = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )
    kind = models.CharField(max_length=200, blank=True, default='ip_address')



    class Meta:
        ordering = ['family', 'address']
        verbose_name = 'IP address'
        verbose_name_plural = 'IP addresses'

    def __str__(self):
        return str(self.address)

    # def get_absolute_url(self, request=None):
    #     return reverse('api:ipam_ip_address-detail', kwargs={'pk': self.pk}, request=request)



    def get_duplicates(self):
        return IPAddress.objects.filter(vrf=self.vrf, address__net_host=str(self.address.ip)).exclude(pk=self.pk)

    def clean(self):

        if self.address:

            # Enforce unique IP space (if applicable)
            if (self.vrf is None and django_settings.ENFORCE_GLOBAL_UNIQUE) or (self.vrf and self.vrf.enforce_unique):
                duplicate_ips = self.get_duplicates()
                if duplicate_ips:
                    raise ValidationError({
                        'address': "Duplicate IP address found in {}: {}".format(
                            "VRF {}".format(self.vrf) if self.vrf else "global table",
                            duplicate_ips.first(),
                        )
                    })

    def save(self, *args, **kwargs):
        if self.address:
            # Infer address family from IPAddress object
            self.family = self.address.version
        super(IPAddress, self).save(*args, **kwargs)



class AhomeJobTemplate(CreatedUpdatedModel):
    """
    Template for all ahome modules
    """
    class Meta:
        abstract = True

    name = models.CharField(max_length=100, blank=True)
    label = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    action = models.CharField(
        max_length=200, 
        blank=True,
        choices=ACTION_CHOICES,
        default='start',
        verbose_name=_('ahomefile action'),
        help_text=_("Infrastructure as a Code action"),
        )
    ahomefile = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
        verbose_name=_('ahomefile'),
        help_text=_("Infrastructure as a Code file"),
    )
    organization = models.ForeignKey(
        ORGANISATION_MODEL,
        related_name='%(class)ss',
        on_delete=models.PROTECT, 
        blank=True, 
        null=True
    )
    target = models.CharField(max_length=200, blank=True)
    kind = models.CharField(max_length=200, default='generic')
    hosted = models.CharField(max_length=200, blank=True)
    opts = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )
    status = models.CharField(
        max_length=200, 
        blank=True,
        choices=STATUS_CHOICES,
        default='running',
    )
    output = models.CharField(max_length=200, blank=True)
    ident = models.CharField(max_length=200, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=True)
    source = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )
    credentials = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )
    definition = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )
    facts = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )
    setfacts = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )
    unique_keys = HStoreField(
        blank=True,
        default=dict,
        null=True,
        verbose_name=_("unique keys"),
        help_text=_("Unique key(s) for ansible callback")
    )
    hosted = models.CharField(max_length=200, blank=True)
    inputs = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )
    schema = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )
    cloud = models.BooleanField(
        verbose_name=_("cloud based"), 
        default=False
    )
    runner = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name=_("tags"),
        blank=True,
        help_text=_("Select tag(s)"),
    )
    # tags = ArrayField(models.CharField(max_length=200), blank=True)





# TODO: import cloud database or set cloud native/based info
    def save(self, *args, **kwargs):
        if self.kind:
            if self.kind in CLOUD_LISTS:
                self.cloud = True
            # load default schema
            if not self.schema:
                self.schema = DEFAULT_CREDENTIAL_SCHEMA

        super(AhomeJobTemplate, self).save(*args, **kwargs)



class Job(CreatedUpdatedModel):
    """
    Jobs
    """
    name    = models.CharField(max_length=100, blank=True)
    ident   = models.UUIDField(primary_key=True, default=uuid.uuid4)
    status  = models.CharField(max_length=100, blank=True)
    rc      = models.CharField(max_length=100, blank=True)
    stats   = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )
    logs = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )
    artifacts = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )
    
    stdout = models.TextField(null=True, blank=True)

    inventory = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )
    command = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )
    organization = models.ForeignKey(
        ORGANISATION_MODEL,
        related_name='%(class)ss',
        on_delete=models.PROTECT, 
        blank=True, 
        null=True
    )
    private_data_dir = models.CharField(max_length=100, blank=True)
    namespace = models.CharField(max_length=100, blank=True)
    kind = models.CharField(max_length=200, blank=True, default='job')

    start_time = models.DateField(auto_now_add=True, blank=True, null=True)
    finish_time = models.DateTimeField(auto_now=True, blank=True, null=True)


    class Meta:
        ordering = ['ident',]
        unique_together = ['ident', 'name', 'organization']

    def __str__(self):
        return str(self.ident)


# {'uuid': 'f7319f4f-9d6e-40a3-bd14-a1046fd6e26f', 'counter': 1, 'stdout': '', 'start_line': 0, 'end_line': 0, 
# 'runner_ident': 'ef7b7d53-ff6e-4d35-8faf-9e0075d5f9ef', 'event': 'runner_on_start', 
# 'event_data': {'task': 'shell', 'task_uuid': '0242ac14-0004-4a71-5d1e-000000000009', 'task_action': 'shell', 'task_args': '', 'task_path': '', 'host': 'localhost', 'pid': 1486}, 
# 'pid': 1486, 'created': '2019-07-29T14:44:49.943344', 'parent_uuid': '0242ac14-0004-4a71-5d1e-000000000009'}



class JobEvent(CreatedUpdatedModel):
    """
    Job Event
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    counter = models.IntegerField(default=0, blank=True)
    stdout = models.TextField(blank=True)
    start_line = models.IntegerField(default=0, blank=True)
    end_line = models.IntegerField(default=0, blank=True)
    runner_ident = models.CharField(max_length=100, blank=True)
    event = models.CharField(max_length=100, blank=True)
    pid = models.IntegerField(default=0, null=True, blank=True)
    parent_uuid = models.CharField(max_length=100, blank=True)
    event_data = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )
    job = models.ForeignKey(
        'Job', 
        related_name='%(class)ss',
        on_delete=models.PROTECT, 
        blank=True, 
        null=True
    )
    namespace = models.CharField(max_length=100, blank=True)
    kind = models.CharField(max_length=200, blank=True, default='job_event')
    # created_time = models.DateField(blank=True, null=True)



    class Meta:
        ordering = ['uuid','counter', 'event']

    def __str__(self):
        return str(self.uuid)


    # def save(self, *args, **kwargs):
    #     if self.runner_ident:
    #         # Ensure the Job exists before saving
    #         job, _ignore = Job.objects.get_or_create(
    #             ident = self.runner_ident,
    #             name = self.runner_ident,
    #             # start_time = datetime.strptime(self.created, '%Y-%m-%d'),
    #             # defaults={'name': 'auto-generated'},
    #         )
    #         self.job = job
    #         # self.created = datetime.strptime(self.created, '%Y-%m-%d')
    #     super(JobEvent, self).save(*args, **kwargs)


        ## TODO: Move to signals


        # libvirt_kvm.workflow_on_event_provider_libvirt_kvm(self, **kwargs)

        # ## Save device facts
        # if self.event == 'runner_on_ok':
        #     if self.namespace == 'Provider.libvirt':
        #         # Gathering facts
        #         if self.event_data.get('task_action') == 'gather_facts' :
        #             # Update Hypvervisors/Devices
        #             obj, _ignore = Device.objects.update_or_create(
        #                 name = self.event_data.get('host'),  fqdn = self.event_data.get('remote_addr'),
        #                 defaults = {
        #                     'facts': self.event_data.get('res'),
        #                     'ident': self.runner_ident,
        #                     },
        #                 )
        #         if self.event_data.get('task_action') == 'debug':
                    
        #             if self.event_data['res'].get('r__guests_xml'):

        #                 for vm in self.event_data['res']['r__guests_xml']['results']:

        #                     obj, _ignore = VirtualMachine.objects.update_or_create(
        #                         name = vm.get('item'),  hosted = self.event_data.get('host'),
        #                         defaults = {
        #                             'definition': json.dumps(xmltodict.parse(vm.get('get_xml'))),
        #                             },
        #                         )

        #             if self.event_data['res'].get('r__guests_status'):

        #                 for vm in self.event_data['res']['r__guests_status']['results']:

        #                     obj, _ignore = VirtualMachine.objects.update_or_create(
        #                         name = vm.get('item'),  hosted = self.event_data.get('host'),
        #                         defaults = {
        #                             'status': vm.get('status'),
        #                             'kind': 'libvirt',
        #                             },
        #                         )

        #             if self.event_data['res'].get('r__netinfo'):

        #                 for network in self.event_data['res']['r__netinfo']['networks']:

        #                     obj, _ignore = Sdn.objects.update_or_create(
        #                         name = network,  hosted = self.event_data.get('host'),
        #                         defaults = {
        #                             'source': self.event_data['res']['r__netinfo']['networks'][network],
        #                             'kind': 'libvirt',
        #                             },
        #                         )




class RunnerTask(CreatedUpdatedModel):
    """
    Runner Task
    """
    uuid    = models.UUIDField(default=uuid.uuid4, editable=False)
    obj     = models.CharField(max_length=100, blank=False, null=False)
    obj_id  = models.IntegerField(default=0, blank=False)
    state   = models.CharField(max_length=100, blank=False, null=False, default='New')
    ident   = models.CharField(max_length=100, blank=False, null=False)
    
    class Meta:
        ordering = ['obj','obj_id', 'state']
        unique_together = ['obj', 'obj_id', 'state', 'ident']

    def __str__(self):
        return str(self.uuid)



 
class Provider(AhomeJobTemplate):
    """
    Provider
    """
    class Meta:
        ordering = ['name',]

    def __str__(self):
        return str(self.name)



class UserCredential(AhomeJobTemplate):
    """
    User Credential
    """
    owner = models.ForeignKey(django_settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name',]
        verbose_name = 'User Credential'
        verbose_name_plural = 'User Credentials'

    def __str__(self):
        return str(self.name)





class UserKey(CreatedUpdatedModel):
    """
    User Keys
    """ 
    USER_SSHKEY  = 'sshkey'
    USER_SECRET  = 'secret'
    USER_CUSTOM  = 'custom'
    USER_STATUS  = [
           (USER_SSHKEY, _('SSH Key')),
           (USER_SECRET, _('Username and Password')),
           (USER_CUSTOM, _('Custom authentication')),
       ]
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True, null=True)
    kind = models.CharField(max_length=200, choices=USER_STATUS, default=USER_SSHKEY)
    organization = models.ForeignKey(
        ORGANISATION_MODEL,
        related_name='userkeys', 
        on_delete=models.PROTECT, 
        blank=True, 
        null=True
    )
    owner = models.ForeignKey(django_settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    schema = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )

    injector = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )

    inputs = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )


    cloud = models.BooleanField(
        verbose_name=_("cloud key"), 
        default=False
    )
    keykind     = models.CharField(max_length=200, default='rsa')
    keysize     = models.IntegerField(default=2048)
    fingerprint = models.CharField(max_length=250, blank=True)
    privatekey  = models.TextField(blank=True, null=True)
    publickey   = models.TextField(blank=True, null=True)
    passphrase  = models.CharField(max_length=250, blank=True, null=True)




    class Meta:
        ordering = ['name']
        verbose_name = 'User Key'
        verbose_name_plural = 'User Keys'


    def __str__(self):
        return self.name


class UserSecret(CreatedUpdatedModel):
    """
    User Secret
    """ 
    USER_SSHKEY  = 'sshkey'
    USER_SECRET  = 'secret'
    USER_CUSTOM  = 'custom'
    USER_STATUS  = [
           (USER_SSHKEY, _('SSH Key')),
           (USER_SECRET, _('Username and Password')),
           (USER_CUSTOM, _('Custom authentication')),
       ]
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True, null=True)
    kind = models.CharField(max_length=200, choices=USER_STATUS, default=USER_SSHKEY)
    fingerprint = models.CharField(max_length=250, blank=True)
    organization = models.ForeignKey(
        ORGANISATION_MODEL,
        related_name='usersecrets', 
        on_delete=models.PROTECT, 
        blank=True, 
        null=True
    )
    owner = models.ForeignKey(django_settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    schema = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )

    injector = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )

    inputs = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )

    cloud = models.BooleanField(
        verbose_name=_("cloud key"), 
        default=False
    )


    class Meta:
        ordering = ['name']
        verbose_name = 'User Secret'
        verbose_name_plural = 'User Secrets'


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.inputs:
            self.inputs = generate_inputs_sshkeys(self.inputs)
        super(UserSecret, self).save(*args, **kwargs)



class IaaS(AhomeJobTemplate):
    """
    Infra as a Service
    """
    # provider = models.ForeignKey(
    #     Provider, 
    #     related_name='%(class)ss',
    #     on_delete=models.PROTECT, 
    #     blank=True, 
    #     null=True
    # )

    usercredential = models.ForeignKey(
        UserCredential, 
        related_name='%(class)ss',
        on_delete=models.PROTECT, 
        blank=True, 
        null=True
    )

    userkey = models.ManyToManyField(
        UserKey, 
        related_name='%(class)ss',
        blank=True, 
    )

    usersecret = models.ManyToManyField(
        UserSecret, 
        related_name='%(class)ss',
        blank=True, 
    )


    class Meta:
        ordering = ['name',]

    def __str__(self):
        return str(self.name)


    def save(self, *args, **kwargs):
        if self.inputs:
            self.inputs = generate_inputs_sshkeys(self.inputs)
        super(IaaS, self).save(*args, **kwargs)



class Sdn(AhomeJobTemplate):
    """
    SDN
    """

    class Meta:
        ordering = ['name',]

    def __str__(self):
        return str(self.name)




class Storage(AhomeJobTemplate):
    """
    Storage
    """
    class Meta:
        ordering = ['name',]

    def __str__(self):
        return str(self.name)

class Service(AhomeJobTemplate):
    """
    Service
    """
    class Meta:
        ordering = ['name',]

    def __str__(self):
        return str(self.name)


class Monitoring(AhomeJobTemplate):
    """
    Monitoring
    """
    class Meta:
        ordering = ['name',]

    def __str__(self):
        return str(self.name)

class Security(AhomeJobTemplate):
    """
    Security
    """
    class Meta:
        ordering = ['name',]

    def __str__(self):
        return str(self.name)


class Pki(AhomeJobTemplate):
    """
    PKI
    """
    class Meta:
        ordering = ['name',]

    def __str__(self):
        return str(self.name)


class Backup(AhomeJobTemplate):
    """
    Backup
    """
    class Meta:
        ordering = ['name',]

    def __str__(self):
        return str(self.name)

class Billing(AhomeJobTemplate):
    """
    Billing
    """
    class Meta:
        ordering = ['name',]

    def __str__(self):
        return str(self.name)


class Documentation(AhomeJobTemplate):
    """
    Documentation
    """
    class Meta:
        ordering = ['name',]

    def __str__(self):
        return str(self.name)






class Credential(CreatedUpdatedModel):
    """
    Credential
    """ 
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True, null=True)
    kind = models.CharField(max_length=200, default='generic')
    organization = models.ForeignKey(
        ORGANISATION_MODEL,
        related_name='credentials', 
        on_delete=models.PROTECT, 
        blank=True, 
        null=True
    )
    inputs = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )
    cloud = models.BooleanField(
        verbose_name=_("cloud credential"), 
        default=False
    )    


    class Meta:
        ordering = ['name']
        verbose_name = 'Credential'
        verbose_name_plural = 'Credentials'


    def __str__(self):
        return self.name



class WizardBox(CreatedUpdatedModel):
    """
    Credential
    """ 
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True, null=True)
    kind = models.CharField(max_length=200, default='generic')
    organization = models.ForeignKey(
        ORGANISATION_MODEL,
        related_name='wizardboxes', 
        on_delete=models.PROTECT, 
        blank=True, 
        null=True
    )
    schema = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )
    inputs = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'WizardBox'
        verbose_name_plural = 'WizardBoxes'


    def __str__(self):
        return self.name










class DeviceTemplate(CreatedUpdatedModel):
    """
    Template for all devices (physical and virtual)
    """
    class Meta:
        abstract = True

    name = models.CharField(max_length=100, blank=True)
    label = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=100, blank=True)
    fqdn = models.CharField(max_length=200, blank=True)
    model = models.CharField(max_length=200, blank=True)
    kind = models.CharField(max_length=200, default='generic')
    uuid = models.UUIDField(default=uuid.uuid4, editable=True, unique=True)
    sn = models.CharField(
        max_length=200, 
        blank=True,
        verbose_name=_('Serial Number'),
        help_text=_("Specifies the serial number of the device if exist"),
        )
    organization = models.ForeignKey(
        ORGANISATION_MODEL,
        related_name='%(class)ss',
        on_delete=models.PROTECT, 
        blank=True, 
        null=True
    )
    credentials = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )
    inputs = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )
    schema = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )

    cloud = models.BooleanField(
        verbose_name=_("cloud based"), 
        default=False
    )   

    primary_ip = models.GenericIPAddressField(null=True, blank=True)
    primary_ip6 = models.GenericIPAddressField(null=True, blank=True)
    primary_mac = models.CharField(max_length=200, blank=True)
    primary_domain = models.CharField(max_length=200, blank=True)

    status = models.CharField(
        max_length=200, 
        blank=True,
        choices=STATUS_CHOICES,
        default='running',
    )

    action = models.CharField(
        max_length=200, 
        blank=True,
        choices=ACTION_CHOICES,
        default='start',
        verbose_name=_('ahomefile action'),
        help_text=_("Infrastructure as a Code action"),
    )

    facts = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )

    setfacts = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )


    ident = models.CharField(max_length=200, blank=True)

    definition = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )

    unique_keys = HStoreField(
        blank=True,
        default=dict,
        null=True,
        verbose_name=_("unique keys"),
        help_text=_("Unique key(s) for ansible callback")
    )

    hosted = models.CharField(max_length=200, null=True , blank=True)
    processors = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )    
    disks = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )
    lvm = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )
    lsblk = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )
    mounts = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )
    memory = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )
    ipaddresses = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )
    ipv4 = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )
    ipv6 = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )        
    interfaces = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )
    svc = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )
    containers = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )
    hardware = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )
    os = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )
    runner = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )

    tags = models.ManyToManyField(
        Tag,
        verbose_name=_("tags"),
        blank=True,
        help_text=_("Select tag(s)")
    )

# TODO: import cloud database or set cloud native/based info
    def save(self, *args, **kwargs):
        if self.kind:
            if self.kind in CLOUD_LISTS:
                self.cloud = True

            # load default schema
            if not self.schema:
                self.schema = DEFAULT_CREDENTIAL_SCHEMA


        super(DeviceTemplate, self).save(*args, **kwargs)




 
class Device(DeviceTemplate):
    """
    BareMetal / Hypervisors /  Appliances / Storage Unit
    """

    provider = models.ForeignKey(
        Provider, 
        related_name='%(class)ss',
        on_delete=models.PROTECT, 
        blank=True, 
        null=True
    )


    virtualmachines = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )

    sdn = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )

    prefixes = JSONField(
        blank=True,
        default=dict,
        editable=True,
        null=True,
    )

    class Meta:
        ordering = ['name',]

    def __str__(self):
        return str(self.name)


class VirtualMachine(DeviceTemplate):
    """
    Virtual Machines
    """

    iaas = models.ForeignKey(
        IaaS, 
        related_name='%(class)ss',
        on_delete=models.PROTECT, 
        blank=True, 
        null=True
    )



    class Meta:
        ordering = ['name',]

    def __str__(self):
        return str(self.name)


class NetworkGear(DeviceTemplate):
    """
    Network Gears
    """
    class Meta:
        ordering = ['name',]

    def __str__(self):
        return str(self.name)


class Container(CreatedUpdatedModel):
    """
    Containers and Pods
    """
    name = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=100, blank=True)
    hosted = models.CharField(max_length=200, blank=True)
    organization = models.ForeignKey(ORGANISATION_MODEL, related_name='containers', on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        ordering = ['name',]


IMPORTANT_MODELS = (
    Sdn,
    IPAddress,
    Prefix,
    Device,
    NetworkGear,
    Rir,
    Vlan,
    Vrf,
    VirtualMachine,
    Job,
    JobEvent,
    Provider,
    Storage,
    Tag,
    Aggregate,
    Container,
    WizardBox,
    Credential,
    Documentation,
    RunnerTask,
    Billing,
    Backup,
    Pki,
    Security,
    Monitoring,
    Service,
    UserSecret,
    UserKey,
    UserCredential
)
