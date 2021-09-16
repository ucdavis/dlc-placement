from django.conf.urls import url
from . import views
 
 
urlpatterns = [
    url(r'^$', views.language_list, name="list"),
    url(r'^create$', views.language_create, name="create"),
    url(r'^(?P<id>\d+)/detail/$', views.language_detail, name="detail"),
    url(r'^(?P<id>\d+)/edit/$', views.language_update, name="edit"),
#    url(r'^(?P<id>\d+)/delete$', views.language_delete, name="delete"),
]
