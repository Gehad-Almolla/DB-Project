from django import template

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    """Return True if the user belongs to the given group name.

    Safely handles AnonymousUser and missing attributes.
    """
    try:
        if user is None:
            return False
        # AnonymousUser has no groups attribute in some setups
        groups = getattr(user, 'groups', None)
        if groups is None:
            return False
        return groups.filter(name=group_name).exists()
    except Exception:
        return False
from django import template

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    """Return True if the user is in the given group name."""
    try:
        if user.is_anonymous:
            return False
        return user.groups.filter(name=group_name).exists()
    except Exception:
        return False
