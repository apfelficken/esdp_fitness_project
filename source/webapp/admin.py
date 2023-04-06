from django.contrib import admin
from webapp.models import Client, Payment, Group, Training, Coach, GroupTraining

admin.site.register(Client)
admin.site.register(Payment)
admin.site.register(Group)
admin.site.register(Training)
admin.site.register(Coach)
admin.site.register(GroupTraining)
