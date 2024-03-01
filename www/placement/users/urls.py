from django.urls import re_path
from . import views
 
 
urlpatterns = [
    re_path(r'^validate/$', views.validate_user, name="validate"),
    re_path(r'^$', views.users_list, name="list"),
    re_path(r'^inactive/$', views.users_inactive, name="inactive"),
    re_path(r'^create$', views.users_create, name="create"),
    re_path(r'^(?P<id>\d+)/detail/$', views.users_detail, name="detail"),
    re_path(r'^account/$', views.users_account, name="account"),
    re_path(r'^(?P<id>\d+)/edit/$', views.users_update, name="edit"),
    re_path(r'^validate/', views.validate_user, name= "validate"),
    re_path(r'^GetUserIAM/(?P<uid>\w+)/$', views.GetUserIAM, name='get_user_iam'),
]
