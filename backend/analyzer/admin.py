from django.contrib import admin

from .models import Hours

# Die Hours Tabelle unter localhost:8000/admin/ sichtbar machen
class HoursAdmin(admin.ModelAdmin):
    search_fields = ['project_id']
    list_display = ('project_id', 'reflection', 'comment', 'start', 'stop')

admin.site.register(Hours, HoursAdmin)