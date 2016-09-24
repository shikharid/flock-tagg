from rest_framework import serializers
# Create your views here.
from taggserver.models import FlockUser, Content, Message, File, Tag


class UserSerializer(serializers.ModelSerializer):
    """
    User Model
    """

    class Meta:
        model = FlockUser
        fields = ('user_token', 'user_id')


class ContentSerializer(serializers.ModelSerializer):
    """
    Content Model
    """

    class Meta:
        model = Content
        fields = ('content_json', 'user', 'id', 'to')


class MessageSerializer(serializers.ModelSerializer):
    """
    Message Serializer
    """

    class Meta:
        model = Message
        fields = ('message_content', 'id')


class FileSerializer(serializers.ModelSerializer):
    """
    File Serializer
    """

    class Meta:
        model = File
        fields = ('file_data', 'id')


class TagSerializer(serializers.ModelSerializer):
    """
    Tag serializer
    """

    class Meta:
        model = Tag
        fields = ('tag_value', 'id')

