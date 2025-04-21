from django.contrib import admin
from .models import Church, Member, Department

# Register your models here.

admin.site.register(Church)
admin.site.register(Member)
admin.site.register(Department)
