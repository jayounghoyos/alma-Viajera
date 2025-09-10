from django import template

register = template.Library()

@register.filter
def to_range(value):
    """Generate a range of numbers from 0 to value."""
    return range(value)