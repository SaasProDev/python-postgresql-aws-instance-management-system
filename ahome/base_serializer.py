import traceback
from logging import getLogger
from collections import OrderedDict
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.fields.related import ForeignObjectRel
from rest_framework import serializers
from rest_framework.reverse import reverse
from django.conf import settings
from sysutils.utils.dict_utils import safeget
from core.utils.common import yaml, to_slugify, load_yml_to_dict

_logger = getLogger(__name__)


AHOMEMAPPINGS_PATH = settings.AHOMEMAPPINGS_PATH
HOURS_IN_MONTH = settings.HOURS_IN_MONTH

DEFAULT_SUMMARY_FIELDS = ('id', 'uuid', 'name', 'kind', 'status') # , 'created_by', 'modified_by')#, 'type')
DEFAULT_RUN_FIELDS = ('synchronize', 'activate', 'deactivate', 'shutdown', 'reconfigure', 'check')

RUN_MODELS = {
    'provider': DEFAULT_RUN_FIELDS,
    'iaas': DEFAULT_RUN_FIELDS + ('deploy',),
    'device': DEFAULT_RUN_FIELDS,
    'virtualmachine': DEFAULT_RUN_FIELDS,
    'usercredential': DEFAULT_RUN_FIELDS,

}


SUMMARIZABLE_FK_FIELDS = {
    'organization': DEFAULT_SUMMARY_FIELDS,
    # 'user': ('id', 'username', 'first_name', 'last_name'),
    # 'application': ('id', 'name'),
    'provider': DEFAULT_SUMMARY_FIELDS,
    'iaas': DEFAULT_SUMMARY_FIELDS + ('inputs',),
    'device': DEFAULT_SUMMARY_FIELDS,
    'virtualmachine': DEFAULT_SUMMARY_FIELDS,
    'usercredential': DEFAULT_SUMMARY_FIELDS,

    # 'inventory': DEFAULT_SUMMARY_FIELDS + ('has_active_failures',
    #                                        'total_hosts',
    #                                        'hosts_with_active_failures',
    #                                        'total_groups',
    #                                        'groups_with_active_failures',
    #                                        'has_inventory_sources',
    #                                        'total_inventory_sources',
    #                                        'inventory_sources_with_failures',
    #                                        'organization_id',
    #                                        'kind',
    #                                        'insights_credential_id',),
    # 'host': DEFAULT_SUMMARY_FIELDS + ('has_active_failures',
    #                                   'has_inventory_sources'),
    # 'group': DEFAULT_SUMMARY_FIELDS + ('has_active_failures',
    #                                    'total_hosts',
    #                                    'hosts_with_active_failures',
    #                                    'total_groups',
    #                                    'groups_with_active_failures',
    #                                    'has_inventory_sources'),

}

RELATED_MAPPING_FIELDS = {
    'organizations': 'organization',
    'rirs': 'rir',
    'vrfs': 'vrf',
    'aggregates': 'aggregate',
    'prefixes': 'prefix',
    'vlans': 'vlans',
    'ip_addresses': 'ip_address',
    'jobs': 'job',
    'providers': 'provider',
    'iaass': 'iaas',
    'sdns': 'sdn',
    'storages': 'storage',
    'services': 'service',
    'monitorings': 'monitoring',
    'securitys': 'security',
    'pkis': 'pki',
    'backups': 'backup',
    'billings': 'billing',
    'documentations': 'documentation',
    'credentials': 'credential',
    'wizardboxes': 'wizardbox',
    'devices': 'device',
    'virtualmachines': 'virtualmachine',
    'networkgears': 'networkgear',
    'containers': 'container',
    'usercredentials': 'user_credential',
    'userkeys': 'user_key',
    'usersecrets': 'user_secret',

    'infrastructures': 'infrastructure',
    'projects': 'project',
}


# Keys are fields (foreign keys) where, if found on an instance, summary info
# should be added to the serialized data.  Values are a tuple of field names on
# the related object to include in the summary data (if the field is present on
# the related object).

class BaseSerializer(serializers.HyperlinkedModelSerializer):
    id             = serializers.ReadOnlyField()
    type           = serializers.SerializerMethodField()
    run            = serializers.SerializerMethodField('_get_run_fields')
    related        = serializers.SerializerMethodField('_get_related')
    summary_fields = serializers.SerializerMethodField('_get_summary_fields')
    frontend       = serializers.SerializerMethodField('_get_frontend')
    instance       = serializers.SerializerMethodField('_get_instance')
    billing        = serializers.SerializerMethodField('_get_billing_info')

    project_info = serializers.SerializerMethodField('_get_project_info')

    def _get_project_info(self, obj):
        try:
            if hasattr(obj, 'project'):
                return {'name': obj.project.name, 'id': obj.project.id, 'uuid': obj.project.uuid}
        except:
            _logger.warning("*** Something not so good - please review ***")
            pass
        return {}

    class Meta:
        fields = '__all__'

    def get_type(self, obj):
        from core.utils.common import get_type_for_model
        return get_type_for_model(self.Meta.model)


    def _get_billing_info(self, obj):
        if not hasattr(obj, 'live_time'):
            return {}
        live_time = obj.live_time()
        if hasattr(obj, 'cost'):
            cost = getattr(obj, 'cost')
            hour_rate = cost
            rate_month = cost * HOURS_IN_MONTH

        elif obj and hasattr(obj, 'inputs') and obj.inputs and obj.inputs.get('costs'):
            # MINIMAL_BILLING_PERIOD_HOURS = 1
            cost = float(obj.inputs.get('costs'))
            rate_month = cost
            hour_rate = cost / HOURS_IN_MONTH
        else:
            return {}

        total = live_time['hours'] * hour_rate

        billing_info = {
            'currency': 'euro',
            'total':   max(round(hour_rate,  4), round(total, 2)),
            'current':  max(round(hour_rate,  4), round(total, 2)),
            'rate_month':  rate_month,
            'live_time': live_time,
            'rate_hour': round(hour_rate, 4),   # todo - update formula - based on summup inluded resources
        }
        return billing_info


    def get_url2(self, obj):
        request = self.context.get('request')
        url = reverse( '{}-detail'.format(obj.__class__.__name__.lower()), args=[obj.pk] )
        return request.build_absolute_uri(url)
        # return reverse( '{}-detail'.format(obj.__class__.__name__.lower()), args=[obj.pk] )

    def _get_related(self, obj):
        return {} if obj is None else self.get_related(obj)

    def get_related(self, obj):
        res = OrderedDict()
        r__fields = [field.get_accessor_name() for field in obj._meta.get_fields() if issubclass(type(field), ForeignObjectRel)]

        # res['debug'] = r__fields
        # rel__fields = list(map(lambda i: i[ : -1], r__fields))

        # rel__fields = list(map(lambda i: RELATED_MAPPING_FIELDS.get(i, i), r__fields))
        # res['debug_related'] = rel__fields

        # _logger.info(f"r__fields: {r__fields}")
        # _logger.info(f"obj: {obj._meta.get_fields()}")


        for r__field in r__fields:
            try:
                interesting_fields = ('id', 'uuid', 'name', 'kind', 'status')

                related__field = RELATED_MAPPING_FIELDS.get(r__field, r__field)
                if related__field in SUMMARIZABLE_FK_FIELDS.keys():
                    r__obj = getattr(obj, "{}".format(r__field), None)
                    actual_fields = [x for x in interesting_fields if hasattr(r__obj, x)]
                    qs = r__obj.all().values('id', 'uuid', 'name', 'kind', 'status')
                    #_logger.info(f"ahome/base_serializer.py BaseSerializer->get_related: actual_fields: {actual_fields}")
                    # qs = r__obj.all().values(*actual_fields)
                    related = []
                    request = self.context.get('request')
                    for item in qs:
                        url = reverse( '{}-detail'.format(related__field), args=[item.get("id")] )
                        data = dict(
                            url = request.build_absolute_uri(url),
                            id = item.get("id"),
                            uuid = item.get("uuid"),
                            name = item.get("name"),
                            kind = item.get("kind"),
                            status = item.get("status"),
                        )
                        related.append(data)
                    res[related__field] = related

            except Exception as ex:
                _logger.error("Exception: {}; {}".format(ex, traceback.format_exc()))
        return res

    def _get_summary_fields(self, obj):
        return {} if obj is None else self.get_summary_fields(obj)

    def get_summary_fields(self, obj):
        # Return values for certain fields on related objects, to simplify
        # displaying lists of items without additional API requests.
        summary_fields = OrderedDict()

        request = self.context.get('request')

        for fk, related_fields in SUMMARIZABLE_FK_FIELDS.items():
            try:
                # A few special cases where we don't want to access the field
                # because it results in additional queries.

                try:
                    fkval = getattr(obj, fk, None)
                except ObjectDoesNotExist:
                    continue
                if fkval is None:
                    continue
                if fkval == obj:
                    continue

                summary_fields[fk] = OrderedDict()

                for field in related_fields:

                    fval = getattr(fkval, field, None)
                    if fval is not None:
                        #remove private key in inputs
                        if field == 'inputs':
                            fval.pop('privatekey', None)
                        if field == 'id':
                            summary_fields[fk]['url'] = request.build_absolute_uri ( reverse( '{}-detail'.format(fk), args=[fval] ) )
                        summary_fields[fk][field] = fval
            # Can be raised by the reverse accessor for a OneToOneField.
            except ObjectDoesNotExist:
                pass

        return summary_fields

    def _get_run_fields(self, obj):
        return {} if obj is None else self.get_run_fields(obj)

    def get_run_fields(self, obj):
        run_fields = OrderedDict()

        obj_name = obj.__class__.__name__.lower()

        request = self.context.get('request')

        # run_fields['activate'] = reverse('{}-run-activate'.format(obj_name), args=[obj.pk])

        if RUN_MODELS.get(obj_name):
            for field in RUN_MODELS.get(obj_name):
                run_fields[field] = request.build_absolute_uri ( reverse('{}-run-{}'.format(obj_name, field), args=[obj.pk]) )

        # run_fields['deploy'] = reverse('{}-run-deploy'.format(obj.__class__.__name__), args=[obj.pk])
        # run_fields['synchronize'] = reverse('{}-run-synchronize'.format(obj.__class__.__name__), args=[obj.pk])
        # run_fields['activate'] = reverse('{}-run-activate'.format(obj.__class__.__name__), args=[obj.pk])
        # run_fields['deactivate'] = reverse('{}-run-deactivate'.format(obj.__class__.__name__), args=[obj.pk])
        # run_fields['shutdown'] = reverse('{}-run-shutdown'.format(obj.__class__.__name__), args=[obj.pk])
        # run_fields['reconfigure'] = reverse('{}-run-reconfigure'.format(obj.__class__.__name__), args=[obj.pk])

        # view.reverse_action('set-password', args=['1'])
        # view.reverse_action(view.DeviceViewSet.run_synchronize, args=[obj.pk])

        return run_fields

    def _get_frontend(self, obj):
        return {} if obj is None else self.get_frontend(obj)

    def get_frontend(self, obj):
        frontend = OrderedDict()
        obj_name = obj.__class__.__name__.lower()

        request = self.context.get('request')

        frontend['create'] = request.build_absolute_uri ( reverse( '{}_{}'.format(obj_name, 'create') ) )
        # require a pk
        for item in ['update', 'delete', 'credential', 'detail', ]:
            try:
                frontend[item] = request.build_absolute_uri ( reverse('{}_{}'.format(obj_name, item), args=[obj.pk]) )
            except Exception as e:
                # raise e
                frontend[item] = None

        # only listing
        for item in ['list', ]:
            try:
                frontend[item] = request.build_absolute_uri (reverse('{}_{}'.format(obj_name, item)) )
            except Exception as e:
                # raise e
                frontend[item] = None

        return frontend

    def _get_instance(self, obj):
        return {} if obj is None else self.get_instance(obj)

# TODO : need to be revamped... load yaml based on kind - to change
    def get_instance(self, obj):
        instance_vars = OrderedDict()

        try:
            if obj.kind:
                ahomefile = "{}/{}.yml".format(AHOMEMAPPINGS_PATH, obj.kind)
            else:
                ahomefile = "{}/generic.yml".format(AHOMEMAPPINGS_PATH)

            map__data = yaml.load(open(ahomefile), Loader=yaml.SafeLoader)

            if map__data:
                if map__data.get("instance_vars"):
                    map__instance_vars = map__data.get("instance_vars")
                    map__schema = obj.schema
                    map__inputs = obj.inputs
                    if map__schema.get('fields') and map__schema.get('fields_advanced'):
                        m = []
                        for item in ['fields', 'fields_advanced' ]:
                            for d in map__schema.get(item, {}):
                                m.append(d)
                        map__schema = m

                    # instance_vars["schema"] = map__schema

                    for instance_key, instance_var in map__instance_vars.items():
                        instance_vars[instance_key] = instance_var

                        map__field = next( ( item for item in map__schema if item["name"] == instance_var ), {} )

                        if map__field.get("type") in ["select" ,]:
                            z = next( ( item for item in map__field.get("choices") if item["value"] == map__inputs.get(instance_var) ), {} )
                            if z:
                                instance_vars["{}".format(instance_key)] = to_slugify( z.get("name") )
                                instance_vars["{}_label".format(instance_key)] = z.get("name")
                                instance_vars["{}_input".format(instance_key)] = z.get("value")
                        else:
                            instance_vars[instance_key] = map__inputs.get(instance_var)

        except Exception as ex:
            _logger.error(" Cannot get instance for obj: {} Exception {}; {}".format(obj, ex, traceback.format_exc()))
            raise

        return instance_vars

    def to_representation(self, instance):
        instance_name = instance.__class__.__name__.lower()
        representation = super().to_representation(instance)

        instance_icons = dict()
        if hasattr(instance, 'kind'):
            instance_icons[instance_name] = dict(
                small = instance.kind,
                large = instance.kind,
                image = instance.kind,
            )
            # todo coode duplicate - FIX / Refactor
            if representation.get("instance"):
                if representation["instance"].get("image"):
                    for item in ["small", "large", "image"]:
                        instance_icons[instance_name].update({ item: representation["instance"].get("image") })
            else:
                if instance.kind:
                    ahomefile = "{}/{}.yml".format(AHOMEMAPPINGS_PATH, instance.kind)
                else:
                    ahomefile = "{}/generic.yml".format(AHOMEMAPPINGS_PATH, instance.kind)

                i = load_yml_to_dict(ahomefile, 'icons')
                for item in ["small", "large", "image"]:
                    if i.get(item):
                        instance_icons[instance_name].update({ item: i.get(item) })

            if representation.get("summary_fields"):
                for instance_name, instance_val in representation["summary_fields"].items():
                    instance_icons[instance_name] = dict(
                        small = instance_val.get("kind"),
                        large = instance_val.get("kind"),
                        image = instance_val.get("kind"),
                    )
                    ahomefile = "{}/{}.yml".format(AHOMEMAPPINGS_PATH, instance_val.get("kind"))
                    i = load_yml_to_dict(ahomefile, 'icons')
                    for item in ["small", "large", "image"]:
                        if i.get(item):
                            instance_icons[instance_name].update({ item: i.get(item) })

        icons = dict()

        for icon_name, icon_val in instance_icons.items():
            icons[icon_name] = dict()

            for item in ["small", "large"]:
                suffix = "-sm.svg" if item == "small" else "-lg.svg"
                icon_url = "{}ahome/assets/{}".format( settings.STATIC_URL, icon_val.get(item) )
                icon_url = "{}".format(icon_url) if str(icon_url).endswith(".svg") else "{}{}".format(icon_url, suffix)
                icons[icon_name].update({item: icon_url})

            suffix = ".svg"
            icon_url = "{}ahome/assets/{}".format( settings.STATIC_URL, icon_val.get("image") )
            icon_url = "{}".format(icon_url) if str(icon_url).endswith(".svg") else "{}{}".format(icon_url, suffix)
            icons[icon_name].update({"image": icon_url})

        representation.update(dict(
                icons=icons
            )
        )

        return representation


# class IaasBaseSerializer(BaseSerializer):
#     project_info = serializers.SerializerMethodField('_get_project_info')
#
#     def _get_project_info(self, obj):
#         result = {'name': obj.project.name, 'id': obj.project.id, 'uuid': obj.project.uuid}
#         return result


class ProjectBaseSerializer(BaseSerializer):
    user_info = serializers.SerializerMethodField('_get_user_info')

    def _get_user_info(self, obj):
        from core.models.models_project import UserProject
        users = UserProject.objects.filter(project_id=obj.id).all()
        result = [{'username': pu.user.username, 'user_id': pu.user.id, 'role': pu.role} for pu in users]
        return result


class OrganizationBaseSerializer(BaseSerializer):
    user_info = serializers.SerializerMethodField('_get_user_info')
    project_info = serializers.SerializerMethodField('_get_project_info')

    def _get_user_info(self, obj):
        from account.models import UserOrganizations
        users = UserOrganizations.objects.filter(organization_id=obj.id).all()
        result = [{'username': pu.user.username, 'user_id': pu.user.id, 'role': pu.role} for pu in users]
        return result

    def _get_project_info(self, obj):
        result = [{'name': p.name, 'id': p.id, 'uuid': p.uuid} for p in obj.projects.all()]
        return result
