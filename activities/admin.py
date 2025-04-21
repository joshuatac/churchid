from django.contrib import admin
from .models import Donation, Event, PrayerRequest, Post ,Announcement 

# Register your models here.

admin.site.register(Donation)
admin.site.register(Event)
admin.site.register(PrayerRequest)
admin.site.register(Post)
admin.site.register(Announcement)