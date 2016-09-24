from rest_framework import status, viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from taggserver.serializer import UserSerializer

class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

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
            headers = self.get_success_headers(serializer.data)

            return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

        except Exception:
            print 'Fuck!'
            return Response({'data': 'User already exists'}, status=status.HTTP_200_OK)

    @detail_route(methods=['get'], url_path='create')
    def get_success(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_200_OK)