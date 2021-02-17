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
from django.conf.urls import include, url

# from django.conf import settings
# from django.conf.urls.static import static
from home import views
from django_cas_ng.views import login, logout

urlpatterns = [
# added for CAS
    url(r'^accounts/login$', login, name='cas_ng_login'),
    url(r'^accounts/logout$', logout, name='cas_ng_logout'),
    url(r'^$', views.index, name= "index"),
    url(r'^home/$', views.SearchForm, name= "home"),
    url(r'^language/', include("languages.urls", namespace="language")),
    url(r'^levels/', include("levels.urls", namespace="levels")),
    url(r'^scoresheet/', include("scoresheet.urls", namespace="scoresheet")),
    url(r'^users/', include("users.urls", namespace="users")),
    url(r'^languages_users/', include("languages_users.urls", namespace="languages_users")),
    url(r'^status/', include("status.urls", namespace="status")),
]
