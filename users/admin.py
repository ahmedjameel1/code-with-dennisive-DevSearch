from django.contrib import admin
from .models import Message, Profile,Skill
# Register your models here.
admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(Message)