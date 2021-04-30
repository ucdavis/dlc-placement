from django.conf.urls import url
from . import views
 
urlpatterns = [
    url(r'^(?P<id>\d+)/edit/$', views.languages_users_update, name="edit"),
]
