from django.urls import re_path
from . import views
 
 
urlpatterns = [
    re_path(r'^$', views.language_list, name="list"),
    re_path(r'^create$', views.language_create, name="create"),
    re_path(r'^(?P<id>\d+)/detail/$', views.language_detail, name="detail"),
    re_path(r'^(?P<id>\d+)/edit/$', views.language_update, name="edit"),
#    re_path(r'^(?P<id>\d+)/delete$', views.language_delete, name="delete"),
]
