from django.contrib import admin

from .models import Hours


class HoursAdmin(admin.ModelAdmin):
    list_display = ('project_id', 'comment', 'start', 'stop')


# Register your models here.
admin.site.register(Hours, HoursAdmin)