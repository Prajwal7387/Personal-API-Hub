from rest_framework import serializers
from ..models import CustomAPI

class CustomAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomAPI
        fields = '__all__'
