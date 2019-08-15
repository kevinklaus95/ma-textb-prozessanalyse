from rest_framework import serializers
from .models import Hours

# Anfragen serialisieren
class HoursSerializer(serializers.ModelSerializer):
  class Meta:
    model = Hours
    fields = ('project_id', 'comment', 'reflection', 'start', 'stop')

