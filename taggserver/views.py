import json

from django.db import transaction
from rest_framework import generics
from rest_framework import status, viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import detail_route, list_route
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from taggserver import serializer as tagg_serializers
from taggserver import models as tagg_models


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class UserAPI(viewsets.ModelViewSet):
    serializer_class = tagg_serializers.UserSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        try:
            print 'request: ', request.data
            user_data = {
                'user_id': request.data.get('userId'),
                'user_token': request.data.get('userToken')
            }
            print 'user_data: ', user_data
            serializer = self.get_serializer(data=user_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            # Create user_token tag to be used in filtering

            tag_serializer = tagg_serializers.TagSerializer(data={'tag_value': request.data.get('userId')})
            tag_serializer.is_valid(raise_exception=True)   
            self.perform_create(tag_serializer)

            headers = self.get_success_headers(serializer.data)

            return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

        except Exception:
            print 'Fuck!'
            return Response({'data': 'User already exists'}, status=status.HTTP_200_OK)

    @detail_route(methods=['get'], url_path='create')
    def get_success(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_200_OK)


class ContentAPI(viewsets.ModelViewSet):
    serializer_class = tagg_serializers.ContentSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = tagg_models.Content.objects.all()

    @staticmethod
    def add_tags(content, user):

        message = tagg_models.Message.objects.get(id=content.get('message'))
        tag_objs = [tagg_models.Tag.objects.get(id=tag) for tag in content.get('tags')]

        for attachment in content.get('attachments'):
            file_obj = tagg_models.File.objects.get(id=attachment)
            for tag in tag_objs:
                file_obj.tags.add(tag)
            file_obj.tags.add(tagg_models.Tag.objects.get(tag_value=user.user_token))
            file_obj.save()

        for tag in tag_objs:
            user.tags.add(tag)
            message.tags.add(tag)

        message.tags.add(tagg_models.Tag.objects.get(tag_value=user.user_token))
        user.save()
        message.save()

    def create(self, request, *args, **kwargs):
        print 'Request: ', request.data
        user = get_object_or_404(tagg_models.FlockUser.objects.all(),
                                 user_id=request.data.get('userId'))

        print 'User: ', user
        content_data = {
            'content_json': request.data.get('content_json'),
            'user': user.id
        }
        serializer = self.get_serializer(data=content_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        self.add_tags(request.data.get('content_json'), user)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):

        content = get_object_or_404(tagg_models.Content.objects.all(),
                                    id=self.kwargs.get(self.lookup_field))

        if content.user.user_token != request.query_params.get('userId'):
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(content)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        return Response({})


class MessageAPI(viewsets.ModelViewSet):
    serializer_class = tagg_serializers.MessageSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = tagg_models.Message.objects.all()

    def create(self, request, *args, **kwargs):
        print 'Request: ', request.data
        user = get_object_or_404(tagg_models.FlockUser.objects.all(),
                                 user_id=request.data.get('userId'))

        if user is None:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        message_data = {
            'message_content': request.data.get('message')
        }
        serializer = self.get_serializer(data=message_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):

        content = get_object_or_404(tagg_models.Message.objects.all(),
                                    id=self.kwargs.get(self.lookup_field))
        try:
            if not request.query_params.get('userId') or \
                            tagg_models.FlockUser.objects.get(user_id=request.query_params.get('userId')) is None:
                return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

            serializer = self.get_serializer(content)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except tagg_models.FlockUser.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_401_UNAUTHORIZED)

    def list(self, request, *args, **kwargs):
        return Response({})


class FileAPI(viewsets.ModelViewSet):
    serializer_class = tagg_serializers.FileSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = tagg_models.File.objects.all()

    def create(self, request, *args, **kwargs):

        return super(FileAPI, self).create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):

        file_obj = get_object_or_404(tagg_models.File.objects.all(),
                                 id=self.kwargs.get(self.lookup_field))
        try:
            if not request.query_params.get('userId') or \
                            tagg_models.FlockUser.objects.get(user_id=request.query_params.get('userId')) is None:
                return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

            serializer = self.get_serializer(file_obj)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except tagg_models.FlockUser.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_401_UNAUTHORIZED)


class TagAPI(viewsets.ModelViewSet):
    serializer_class = tagg_serializers.TagSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = tagg_models.Tag.objects.all()

    def create(self, request, *args, **kwargs):

        return super(TagAPI, self).create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):

        tag = get_object_or_404(tagg_models.Tag.objects.all(),
                                id=self.kwargs.get(self.lookup_field))
        try:
            if not request.query_params.get('userId') or \
                            tagg_models.FlockUser.objects.get(user_id=request.query_params.get('userId')) is None:
                return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

            serializer = self.get_serializer(tag)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except tagg_models.FlockUser.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_401_UNAUTHORIZED)

    def list(self, request, *args, **kwargs):
        try:
            if not request.query_params.get('userId') or \
                            tagg_models.FlockUser.objects.get(user_id=request.query_params.get('userId')) is None:
                return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

            return super(TagAPI, self).list(request, *args, **kwargs)
        except tagg_models.FlockUser.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_401_UNAUTHORIZED)

    def filter_queryset(self, queryset):
        queryset = queryset.filter(user__user_id=self.request.query_params.get('userId', 0))
        return super(TagAPI, self).filter_queryset(queryset)


class SearchAPI(viewsets.GenericViewSet):
    file_queryset = tagg_models.File.objects.all()
    message_queryset = tagg_models.Message.objects.all()
    serializer_class = tagg_serializers.TagSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_file_queryset(self):
        queryset = self.file_queryset
        queryset = queryset.all()
        return queryset

    def get_message_queryset(self):
        queryset = self.message_queryset
        queryset = queryset.all()
        return queryset

    @list_route(methods=['post'], url_path='file')
    def search_file(self, request, *args, **kwargs):
        if not request.data.get('userId'):
            return Response({})

        tag_list = request.data.get('tags')
        queryset = self.get_file_queryset().filter(tags__tag_value=request.data.get('userId'))
        for tag in tag_list:
            queryset = queryset.filter(tags__id=tag)

        serializer = tagg_serializers.FileSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @list_route(methods=['post'], url_path='message')
    def search_message(self, request, *args, **kwargs):

        if not request.data.get('userId'):
            return Response({})

        tag_list = request.data.get('tags')
        queryset = self.get_message_queryset().filter(tags__tag_value=request.data.get('userId'))

        for tag in tag_list:
            queryset = queryset.filter(tags__id=tag)

        serializer = tagg_serializers.MessageSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




