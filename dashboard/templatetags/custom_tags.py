from django import template
from django.urls import resolve

register = template.Library()

@register.simple_tag
def active_link(request, url_name, active_class):
    if resolve(request.path_info).url_name == url_name:
        return active_class
    return ''
