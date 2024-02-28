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

app_name = 'placement'
urlpatterns = [
# added for CAS
    url(r'^accounts/login$', login, name='cas_ng_login'),
    url(r'^accounts/logout$', logout, name='cas_ng_logout'),
    url(r'^$', views.index, name= "index"),
    url(r'^home/$', views.SearchForm, name= "home"),
    url(r'^language/', include(("languages.urls", app_name), namespace="language")),
    url(r'^levels/', include(("levels.urls", app_name), namespace="levels")),
    url(r'^scoresheet/', include(("scoresheet.urls", app_name), namespace="scoresheet")),
    url(r'^users/', include(("users.urls", app_name), namespace="users")),
    url(r'^languages_users/', include(("languages_users.urls", app_name), namespace="languages_users")),
    url(r'^status/', include(("status.urls", app_name), namespace="status")),
]
