from django.contrib import admin

# Register your models here.
from django.contrib import admin
from web.models import Box, Command

# Register your models here.


class BoxAdmin(admin.ModelAdmin):
    list_display = ('_id', 'shell')


class CommandAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'box', 'command', 'run_time')


admin.site.register(Box, BoxAdmin)
admin.site.register(Command, CommandAdmin)
