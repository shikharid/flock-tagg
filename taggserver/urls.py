from django.contrib import admin
from django.conf.urls import patterns, include, url

from taggserver import views
admin.autodiscover()


# See: https://docs.djangoproject.com/en/dev/topics/http/urls/
urlpatterns = patterns(
    '',
    url(r'^register/', views.UserView.as_view({'post': 'create', 'get': 'get_success'}),
        name='user-create'),
)
