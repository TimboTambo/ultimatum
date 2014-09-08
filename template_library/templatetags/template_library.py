from django import template
import datetime
import re

register = template.Library()


#Example, would be used like {{variable|cut:" "}} to cut spaces
@register.filter(name='cut')
def cut(value, arg):
    "Removes all values of arg from the given string"
    return value.replace(arg, "")

# Example 2
@register.filter(name="lower2")
def lower2(value):
    "Converts a string to lowercase"
    return value.lower()

@register.filter
def percentage(value, arg):
    "Returns value as a percentage of arg"
    try:
        numerator = float(value)
        denominator = float(arg)
    except ValueError:
        return "ValueError"
    return str(int(round(numerator/denominator*100)))