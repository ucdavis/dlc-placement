"""placement URL Configuration
   URLs for Levels App
"""

from django.conf.urls import url
from . import views
 
 
urlpatterns = [
     url(r'^(?P<id>\d+)$', views.level_list, name="list"),
     url(r'^(?P<id>\d+)/create/$', views.level_create, name="create"),
     url(r'^(?P<id>\d+)/detail/$', views.level_detail, name="detail"),
     url(r'^(?P<id>\d+)/edit/$', views.level_update, name="edit"),
#     url(r'^csv/$', views.csv, name="csv"),
#     url(r'^(?P<id>\d+)/delete$', views.post_delete, name="delete"),
]
