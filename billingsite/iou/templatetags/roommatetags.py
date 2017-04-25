from django import template

register = template.Library()

@register.simple_tag
def get_OwedTo(roommate, owedto):
    return roommate.iouGetOwedTo(owedto)
