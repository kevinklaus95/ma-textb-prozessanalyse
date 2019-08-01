from rest_framework import serializers
from .models import Hours

class HoursSerializer(serializers.ModelSerializer):
  class Meta:
    model = Hours
    fields = ('project_id', 'comment', 'start', 'stop')

