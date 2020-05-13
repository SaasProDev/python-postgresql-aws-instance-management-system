from django import template
from frontend.views.functions import OPS, get_apidata, save_form
import ast

register = template.Library()


@register.filter(name='concatenate')
def concatenate(value, arg):
    """Concatenate all values of arg from the given string"""
    return "{}{}".format(value, arg)

@register.filter(name='cut')
def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, '')

@register.filter(name='slug_js')
def slug_js(value):
    """Removes all values of arg from the given string"""
    return value.replace('-', '_').replace(' ', '_')


@register.filter(name='keyvalue')
def keyvalue(dict, key):    
    try:
        # return dict[key]
        x = ast.literal_eval(dict)
        return x.get('key', 'None')
    except KeyError:
        return ''


@register.filter(name='wz_fields_required')
def wz_fields_required(fields):
    """Return the join required fields for js validation """
    output = []
    for field in fields:
    	# attrs = vars(field.field)
    	# output.append(attrs)
    	if field.field.required:
    		s = field.auto_id.replace('-', '_').replace(' ', '_')
    		s = '($(self.modal + " #%s").val())' % s 
    		output.append(s)

    s = ' && '.join(str(x) for x in output)
    js = "if (%s) { $enable = 1; };" % s

    return js

@register.filter(name='ws_pficon')
def ws_pficon(alert):
    if alert == 'successful':
        return 'pficon-ok'
    elif alert == 'failed':
        return 'pficon-error-circle-o'
    else:
        return 'pficon-info'


@register.filter(name='ws_toast')
def ws_toast(alert):
    if alert == 'successful':
        return 'alert-success'
    elif alert == 'failed':
        return 'alert-danger'
    else:
        return 'alert-info'



@register.inclusion_tag('frontend/includes/helpers/snippet__row_header_spinner.html', takes_context=True)
def snippet__row_header_spinner(context):
    return {
        'data': context['data'],
        'model_name': context['model_name'],
        'url_create': context['url_create'],
        'url_update': context['url_update'],
        'url_delete': context['url_delete'],
    }


@register.inclusion_tag('frontend/includes/helpers/snippet__row_header_spinner_adv.html', takes_context=True)
def snippet__row_header_spinner_adv(context):
    return {
        'data': context['data'],
        'model_name': context['model_name'],
        'url_create': context['url_create'],
        'url_update': context['url_update'],
        'url_delete': context['url_delete'],
    }




@register.inclusion_tag('frontend/includes/helpers/snippet__row_content_progressbar.html', takes_context=True)
def snippet__row_content_progressbar(context):
    return {
        'data': context['data'],
        'model_name': context['model_name'],
        'url_create': context['url_create'],
        'url_update': context['url_update'],
        'url_delete': context['url_delete'],

    }


@register.inclusion_tag('frontend/includes/helpers/snippet_ahome_pricing_plan.html')
def snippet_ahome_pricing_plan():
    pass


    # $el = $(self.modal + " #{{ field.auto_id | slug_js }}");



@register.inclusion_tag('frontend/includes/helpers/snippet__tabs_images.html')
def snippet__tabs_images(request, group_name):

    images = get_apidata('provisioning/iaac/distros/{}/list'.format(group_name), request)
    
    return { 
       'request': request,
       'group_name': group_name,
       'images': images,
    }


@register.inclusion_tag('frontend/includes/helpers/snippet__tabs_pricings.html')
def snippet__tabs_pricings(request, provider, plan_name):

    plans = get_apidata('provisioning/iaac/pricing/{}/{}/list'.format(provider, plan_name), request)
    
    return { 
       'request': request,
       'provider': provider,
       'plan_name': plan_name,
       'plans': plans,
    }


