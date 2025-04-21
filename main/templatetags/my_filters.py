from django import template
from users.models import Member
from activities.models import PrayerRequest




register = template.Library()

@register.simple_tag(takes_context=True)
def get_new_members(context):
    request = context.get('request')  # Get the request object
    members = Member.objects.filter(new=True, church = request.user.church, is_staff=False)
    return  members

@register.simple_tag(takes_context=True)
def get_new_prayers(context):
    request = context.get('request')  # Get the request object
    prayers = PrayerRequest.objects.filter(new=True, church = request.user.church)
    return  prayers