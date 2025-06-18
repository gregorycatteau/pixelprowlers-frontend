from rest_framework import serializers
from .models import DesignTheme

class DesignThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignTheme
        fields = '__all__'
