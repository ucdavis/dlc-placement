from django.urls import re_path

from . import views
 
urlpatterns = [
    re_path(r'^(?P<id>\d+)/edit/$', views.languages_users_update, name="edit"),
]
