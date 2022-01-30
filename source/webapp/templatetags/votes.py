from django import template

register = template.Library()


@register.filter
def voted_by(obj, user):
    return obj.voted_by(user)
