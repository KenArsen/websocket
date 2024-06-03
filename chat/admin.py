from django.contrib import admin
from .models import Group, GroupProfile, Profile, Message

admin.site.register(Group)
admin.site.register(Message)
admin.site.register(GroupProfile)
admin.site.register(Profile)
