"""placement URL Configuration
   URLs for Levels App
"""

from django.urls import re_path
from . import views
 
 
urlpatterns = [
     re_path(r'^(?P<id>\d+)$', views.level_list, name="list"),
     re_path(r'^(?P<id>\d+)/create/$', views.level_create, name="create"),
     re_path(r'^(?P<id>\d+)/detail/$', views.level_detail, name="detail"),
     re_path(r'^(?P<id>\d+)/edit/$', views.level_update, name="edit"),
#     re_path(r'^csv/$', views.csv, name="csv"),
#     re_path(r'^(?P<id>\d+)/delete$', views.post_delete, name="delete"),
]
