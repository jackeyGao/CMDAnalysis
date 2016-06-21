# -*- coding: utf-8 -*-
'''
File Name: web/templatetags/tools.py
Author: JackeyGao
mail: gaojunqi@outlook.com
Created Time: 四  6/16 10:52:51 2016
'''
import json
from django import template

register = template.Library()

@register.filter
def value(data, key):
    value= data.get(key, None)
    if value:
        return value.strip()
    return value 

@register.filter
def gen_url_from_reference(ref):
    reference = ref.replace('[', '').replace(']', '')
    slice_ref = reference.split(',')
    if len(slice_ref) == 0:
        return None
    elif len(slice_ref) == 1:
        return "https://tools.ietf.org/html/%s" % slice_ref[0]
    elif len(slice_ref) == 2:
        rfc, section = slice_ref
    section = section.lower().strip().replace(' ', '-')
    return "https://tools.ietf.org/html/%s#%s" % (rfc, section)

@register.filter
def get_reference(ref):
    reference = ref.replace('[', '').replace(']', '')
    rfc = reference.split(',')[0]
    return rfc

@register.filter
def is_json(jsonstring):
	try:
	    data = json.loads(jsonstring)
	except Exception as e:
		return False
	return True

@register.filter
def to_json(jsonstring):
	try:
	    data = json.loads(jsonstring)
	    return json.dumps(data, indent=2, ensure_ascii=False)
	except Exception as e:
		return None

