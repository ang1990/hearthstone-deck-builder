from rest_framework.serializers import ModelSerializer
from .models import HearthstoneCard





class HearthstoneCardSerializer(ModelSerializer):
    class Meta:
        model = HearthstoneCard