from django.contrib import admin

from app.models import *

# Register your models here.

class AppAdmin(admin.ModelAdmin):
    list_display = ('appid', 'access', 'secret', 'state')
admin.site.register(App, AppAdmin)


