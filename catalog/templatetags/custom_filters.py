from django import template

register = template.Library()


@register.filter
def add_media(value):
    if value:
        return f"/media/{value}"
    return "#"
