from django import template

register = template.Library()

@register.filter
def add_class(value, arg):
    return value + ' ' + arg
