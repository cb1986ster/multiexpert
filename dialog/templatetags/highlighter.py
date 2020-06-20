from django import template
import re

register = template.Library()

@register.filter
def highlight_for_found(statement, q):
    return re.compile(re.escape(q.lower()), re.IGNORECASE).sub(
        '<span class="badge badge-info">{}</span>'.format(q),
         statement.text
    )
