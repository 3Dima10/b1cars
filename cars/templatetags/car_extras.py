from django import template

register = template.Library()


@register.filter
def spacegroup(value):
    try:
        value = int(value)
    except (TypeError, ValueError):
        return value
    return f"{value:,}".replace(",", " ")
