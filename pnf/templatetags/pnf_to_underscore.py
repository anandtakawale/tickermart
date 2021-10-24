from django import template

register = template.Library()

@register.filter
def pnf_to_underscore(value):
    return value.replace("&","_").replace("-", "_")