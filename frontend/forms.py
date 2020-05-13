from django import forms
from django.contrib.auth.models import Permission, Group
from django.contrib.auth import get_user_model
from core.models import *

import json

from django.forms import Textarea

from django.core.validators import MinValueValidator, MaxValueValidator


ORGANISATION_MODEL = 'account.Organization'

User = get_user_model()

jstr="""
{
        "name": "firstname",
        "label": "First Name",
        "type": "text",
        "max_length": 25,
        "required": 1
    }
"""

#-----
class GenerateRandomVirtualMachineForm(forms.Form):
    total = forms.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

#-----


class WizardForm(forms.Form):


    def __init__(self, jsonform, initial, *args, **kwargs):

        super().__init__(*args, **kwargs)

        
        try:
            fields = json.loads(jsonform)
        except Exception as e:
            #raise e
            jsonform = json.dumps(jsonform)
            fields = json.loads(jsonform)
            # fields = json.loads(json.dumps(jsonform))

        # must be a list

        # print ("jsonform --- {} -- fields -- {}".format(type(jsonform), type(fields)))
        # print(fields)

        for field in fields:
            options = self.get_options(field,initial)
            f = getattr(self, "create_field_for_"+field['type'] )(field, options)
            self.fields[field['name']] = f


    def get_options(self, field, initial):
        options = {}
        options['label'] = field.get("label", None)
        options['help_text'] = field.get("help_text", None)
        options['required'] = bool(field.get("required", 0) )

        # Default  value / default or initial
        if field.get("default"):
            options['initial'] = field.get("default")            
        if field.get("initial"):
            options['initial'] = field.get("initial")

        # initial value
        if initial.get(field['name']):
            options['initial'] = initial[field['name']]
        return options

    def create_field_for_text(self, field, options):
        options['max_length'] = int(field.get("max_length", "200") )
        return forms.CharField(**options)

    def create_field_for_password(self, field, options):
        options['max_length'] = int(field.get("max_length", "200") )
        return forms.CharField(widget=forms.PasswordInput(render_value = True), **options)


    def create_field_for_textarea(self, field, options):
        options['max_length'] = int(field.get("max_value", "9999") )
        return forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), **options)

    def create_field_for_integer(self, field, options):
        options['max_value'] = int(field.get("max_value", "999999999") )
        options['min_value'] = int(field.get("min_value", "-999999999") )
        return forms.IntegerField(**options)

    def create_field_for_radio(self, field, options):
        options['choices'] = [ (c['value'], c['name'] ) for c in field['choices'] ]
        return forms.ChoiceField(widget=forms.RadioSelect, **options)

    def create_field_for_select(self, field, options):
        options['choices']  = [ (c['value'], c['name'] ) for c in field['choices'] ]
        attrs = {
                    'class': "selectpicker extra-widget-dropdown",
                }        
        return forms.ChoiceField(widget=forms.Select(attrs=attrs), **options)

    def create_field_for_checkbox(self, field, options):
        return forms.BooleanField(widget=forms.CheckboxInput, **options)

    def create_field_for_modelchoice(self, field, options):
        return forms.ModelChoiceField(queryset=Device.objects.all(), empty_label="(Nothing)", to_field_name="name", **options)

    def create_field_for_modelmultiplechoice(self, field, options):
        return forms.ModelMultipleChoiceField(queryset=Device.objects.all(), to_field_name="name", **options)
    

class FieldHandler():
    
    formfields = {}

    def __init__(self, fields):
        for field in fields:
            options = self.get_options(field)
            f = getattr(self, "create_field_for_"+field['type'] )(field, options)
            self.formfields[field['name']] = f

    def get_options(self, field):
        options = {}
        options['label'] = field['label']
        options['help_text'] = field.get("help_text", None)
        options['required'] = bool(field.get("required", 0) )
        
        # Default  value / default or initial
        if field.get("default"):
            options['initial'] = field.get("default")            
        if field.get("initial"):
            options['initial'] = field.get("initial")

        return options


    def create_field_for_password(self, field, options):
        options['max_length'] = int(field.get("max_length", "200") )
        return forms.CharField(widget=forms.PasswordInput, **options)


    def create_field_for_text(self, field, options):
        options['max_length'] = int(field.get("max_length", "200") )
        return forms.CharField(**options)

    def create_field_for_textarea(self, field, options):
        options['max_length'] = int(field.get("max_value", "9999") )
        return forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), **options)

    def create_field_for_integer(self, field, options):
        options['max_value'] = int(field.get("max_value", "999999999") )
        options['min_value'] = int(field.get("min_value", "-999999999") )
        return forms.IntegerField(**options)

    def create_field_for_radio(self, field, options):
        options['choices'] = [ (c['value'], c['name'] ) for c in field['choices'] ]
        return forms.ChoiceField(widget=forms.RadioSelect, **options)

    def create_field_for_select(self, field, options):
        options['choices']  = [ (c['value'], c['name'] ) for c in field['choices'] ]
        attrs = {
                    'class': "selectpicker extra-widget-dropdown",
                }
        return forms.ChoiceField(widget=forms.Select(attrs=attrs), **options)

    def create_field_for_checkbox(self, field, options):
        return forms.BooleanField(widget=forms.CheckboxInput, **options)


    def create_field_for_modelchoice(self, field, options):
        return forms.ModelChoiceField(queryset=Device.objects.all(), empty_label="(Nothing)", to_field_name="name", **options)

    def create_field_for_modelmultiplechoice(self, field, options):
        return forms.ModelMultipleChoiceField(queryset=Device.objects.all(), to_field_name="name", **options)


def get_form(jstr):
    fields=json.loads(jstr)
    fh = FieldHandler(fields)
    return type('WizardForm', (forms.Form,), fh.formfields )


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "password"] #"teams",


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = "__all__"


class OrganizationForm(forms.ModelForm):
    class Meta:
        from account.models import Organization
        model = Organization
        fields = ('headquarter', 'name', 'description', 'location', 'contact', 'email', 'info', )


class ProjectForm(forms.ModelForm):
    class Meta:
        from core.models import Project
        model = Project
        # fields = ('name', 'description', 'organization')
        fields = ('name', 'description')

        # organisations


class VrfForm(forms.ModelForm):
    class Meta:
        model = Vrf
        fields = ('project', 'name', 'description', 'rd', 'enforce_unique',  )


class RirForm(forms.ModelForm):
    class Meta:
        model = Rir
        fields = ('project', 'name', 'description', 'registry', 'region',  )


class PrefixForm(forms.ModelForm):
    class Meta:
        model = Prefix
        fields = ('project', 'prefix', 'description', 'vrf', 'status', 'vlan', 'is_pool'  )


class AggregateForm(forms.ModelForm):
    class Meta:
        model = Aggregate
        fields = ('project', 'prefix', 'description', 'rir',  )


class IPAddressForm(forms.ModelForm):
    class Meta:
        model = IPAddress
        fields = ('project', 'address', 'description', 'vrf', 'status',  )


class VlanForm(forms.ModelForm):
    class Meta:
        model = Vlan
        fields = ('project', 'vid', 'description', 'status',  )


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ('project', 'name', 'label', 'description',  )


class VirtualMachineForm(forms.ModelForm):
    class Meta:
        model = VirtualMachine
        fields = ('project', 'name', 'description',  )


class NetworkGearForm(forms.ModelForm):
    class Meta:
        model = NetworkGear
        fields = ('project', 'name', 'description',  )


class ContainerForm(forms.ModelForm):
    class Meta:
        model = Container
        fields = ( 'organization', 'name', 'description',  )





class ProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        #fields = ( 'organization', 'name', 'description',  )
        fields = ('name', 'description',  )



class IaaSForm(forms.ModelForm):
    class Meta:
        model = IaaS
        fields = ( 'iaas', 'usercredential', 'name', 'description',  )


class PaaSForm(forms.ModelForm):
    class Meta:
        model = PaaS
        fields = ( 'usercredential', 'name', 'description',  )



class SdnForm(forms.ModelForm):
    class Meta:
        model = Sdn
        fields = ( 'iaas', 'name', 'description',  )




class StorageForm(forms.ModelForm):
    class Meta:
        model = Storage
        fields = ( 'iaas', 'name', 'description',  )




class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ( 'iaas', 'name', 'description',  )




class MonitoringForm(forms.ModelForm):
    class Meta:
        model = Monitoring
        fields = ( 'iaas', 'name', 'description',  )




class SecurityForm(forms.ModelForm):
    class Meta:
        model = Security
        fields = ( 'iaas', 'name', 'description',  )




class PkiForm(forms.ModelForm):
    class Meta:
        model = Pki
        fields = ( 'iaas', 'name', 'description',  )



class BackupForm(forms.ModelForm):
    class Meta:
        model = Backup
        fields = ( 'iaas', 'name', 'description',  )




class BillingForm(forms.ModelForm):
    class Meta:
        model = Billing
        fields = ( 'iaas', 'name', 'description',  )



class DocumentationForm(forms.ModelForm):
    class Meta:
        model = Documentation
        fields = ( 'iaas', 'name', 'description',  )



class CredentialForm(forms.ModelForm):
    class Meta:
        model = Credential
        fields = ( 'name', 'description',  )


class UserCredentialForm(forms.ModelForm):
    class Meta:
        model = UserCredential
        fields = ('name', 'description')    # 'owner',


class UserSecretForm(forms.ModelForm):
    class Meta:
        model = UserSecret
        fields = ( 'owner', 'name', 'description',  )

class UserKeyForm(forms.ModelForm):
    class Meta:
        model = UserKey
        fields = ( 'owner', 'name', 'description', 'privatekey', 'publickey', 'passphrase' )
        widgets = {
            'privatekey': Textarea(attrs={'rows': 4}),
            'publickey': Textarea(attrs={'rows': 4}),
        }


class WizardBoxForm(forms.ModelForm):
    class Meta:
        model = WizardBox
        fields = ( 'name', 'description',  )



