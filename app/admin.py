from django.contrib import admin

from app.models import *

# Register your models here.

class AppAdmin(admin.ModelAdmin):
    list_display = ('appid', 'access', 'secret', 'state')
admin.site.register(App, AppAdmin)

class InviteCodeAdmin(admin.ModelAdmin):
    list_display = ("uid", "code", "app", "create_date")
admin.site.register(InviteCode, InviteCodeAdmin)

class InviteEchoAdmin(admin.ModelAdmin):
    list_display = ("uid", "echo_uid", "read_statu", "app", "create_date")
admin.site.register(InviteEcho, InviteEchoAdmin)


