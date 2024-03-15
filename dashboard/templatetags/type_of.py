# In your Django app, create a templatetags folder (if not exists) and add a new file, e.g., custom_filters.py

# custom_filters.py
from django import template

register = template.Library()

@register.filter
def type_of(value):
    return type(value).__name__
