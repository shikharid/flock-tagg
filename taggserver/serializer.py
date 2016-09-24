from rest_framework import serializers
# Create your views here.
from taggserver.models import FlockUser


class UserSerializer(serializers.ModelSerializer):
    """
    User Model
    """

    class Meta:
        model = FlockUser
        fields = ('user_token', 'user_id')
