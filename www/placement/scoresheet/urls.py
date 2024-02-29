"""placement URL Configuration
   URLs for Scoresheet App
   
   Created on Feb 2016
    @author: mauricio
"""

from django.urls import re_path
from . import views
  
urlpatterns = [
     re_path(r'^list/$', views.scoresheet_list, name="list"),
     re_path(r'^create/$', views.scoresheet_create, name="create"),
     re_path(r'^get_levels/(?P<language_id>\d+)/$', views.get_levels, name='get_levels'),
     re_path(r'^GetStudentBanner/(?P<sid>\d+)/(?P<formatted>\w+)/$', views.GetStudentBanner, name='get_student'),
     re_path(r'^GetStudentInfoFromEmail/(?P<email>\w+|[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', views.GetStudentInfoFromEmail, name='get_student_info_from_email'),
     re_path(r'^(?P<id>\d+)/detail/$', views.scoresheet_detail, name="detail"),
     re_path(r'^(?P<id>\d+)/edit/$', views.scoresheet_update, name="edit"),
     re_path(r'^(?P<id>\d+)/delete$', views.scoresheet_delete, name="delete"),
     re_path(r'^bulk_input/', views.scoresheet_bulk_input, name= "bulk_input"),
]