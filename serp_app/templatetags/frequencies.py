import json

from django import template

register = template.Library()


@register.filter
def frequencies(input, *args, **kwargs):
    html = ''
    inp = json.loads(input)
    for elem in inp:
        # html += f'<p>{elem}</p>'
        html += f'<p>{elem[0]}: {elem[1]} times</p>'
    return html