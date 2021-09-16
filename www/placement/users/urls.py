from django.conf.urls import url
from . import views
 
 
urlpatterns = [
    url(r'^validate/$', views.validate_user, name="validate"),
    url(r'^$', views.users_list, name="list"),
    url(r'^inactive/$', views.users_inactive, name="inactive"),
    url(r'^create$', views.users_create, name="create"),
    url(r'^(?P<id>\d+)/detail/$', views.users_detail, name="detail"),
    url(r'^account/$', views.users_account, name="account"),
    url(r'^(?P<id>\d+)/edit/$', views.users_update, name="edit"),
    url(r'^validate/', views.validate_user, name= "validate"),
    url(r'^GetUserLDAP/(?P<uid>\w+)/$', views.GetUserLDAP, name='get_user_ldap'),
]
