from django.contrib import admin
from django.conf.urls import patterns, include, url

from taggserver import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.include_root_view = False

# Base_name is required as queryset is not set
router.register(r'user', views.UserAPI, 'user')
router.register(r'content', views.ContentAPI, 'content')
router.register(r'message', views.MessageAPI, 'message')
router.register(r'file', views.FileAPI, 'file')
router.register(r'tag', views.TagAPI, 'tag')
router.register(r'search', views.SearchAPI, 'search')

# See: https://docs.djangoproject.com/en/dev/topics/http/urls/
urlpatterns = patterns(
    '',
)

urlpatterns += router.urls
