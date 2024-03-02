"""placement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import include, re_path

# from django.conf import settings
# from django.conf.urls.static import static
from home import views
from django_cas_ng.views import login, logout

app_name = 'placement'
urlpatterns = [
# added for CAS
    re_path(r'^accounts/login$', login, name='cas_ng_login'),
    re_path(r'^accounts/logout$', logout, name='cas_ng_logout'),
    re_path(r'^$', views.index, name= "index"),
    re_path(r'^home/$', views.SearchForm, name= "home"),
    re_path(r'^language/', include(("languages.urls", app_name), namespace="language")),
    re_path(r'^levels/', include(("levels.urls", app_name), namespace="levels")),
    re_path(r'^scoresheet/', include(("scoresheet.urls", app_name), namespace="scoresheet")),
    re_path(r'^users/', include(("users.urls", app_name), namespace="users")),
    re_path(r'^languages_users/', include(("languages_users.urls", app_name), namespace="languages_users")),
    re_path(r'^status/', include(("status.urls", app_name), namespace="status")),
]
