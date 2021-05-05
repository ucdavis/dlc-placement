"""placement URL Configuration
   URLs for Scoresheet App
   
   Created on Feb 2016
    @author: mauricio
"""

from django.conf.urls import url
from . import views
  
urlpatterns = [
     url(r'^list/$', views.scoresheet_list, name="list"),
     url(r'^create/$', views.scoresheet_create, name="create"),
     url(r'^get_levels/(?P<language_id>\d+)/$', views.get_levels, name='get_levels'),
     url(r'^GetStudentBanner/(?P<sid>\d+)/(?P<formatted>\w+)/$', views.GetStudentBanner, name='get_student'),
     url(r'^(?P<id>\d+)/detail/$', views.scoresheet_detail, name="detail"),
     url(r'^(?P<id>\d+)/edit/$', views.scoresheet_update, name="edit"),
     url(r'^(?P<id>\d+)/delete$', views.scoresheet_delete, name="delete"),
     url(r'^bulk_input/', views.scoresheet_bulk_input, name= "bulk_input"),
]