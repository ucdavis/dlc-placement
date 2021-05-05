"""placement URL Configuration
   URLs for Status
   
   Created on January 2020
    @author: ednperez
"""

from django.conf.urls import url
from . import views
  
urlpatterns = [
     url("", views.health, name="health"),
]