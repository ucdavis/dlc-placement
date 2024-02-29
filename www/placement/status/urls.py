"""placement URL Configuration
   URLs for Status
   
   Created on January 2020
    @author: ednperez
"""

from django.urls import path
from . import views
  
urlpatterns = [
     path("", views.health, name="health"),
]