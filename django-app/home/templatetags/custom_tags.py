from django import template

register = template.Library()

# @register.filter(name='get_item')
# def get_item(dictionary, key):
#     return dictionary.get(key, '')

@register.filter(name='get_range')
def get_range(value):
    """Generates a range of numbers from 0 to the specified value - 1."""
    return range(value)