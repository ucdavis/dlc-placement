from __future__ import unicode_literals
from django.urls import reverse
from django.db import models

# Create your models here.

class Users(models.Model):
    id = models.AutoField(primary_key=True, unique=True) # AutoField?
    cas_user = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=254, blank = True)
    advisor = models.BooleanField(default = False)
    tester = models.BooleanField(default = False)
    admin = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)    
    active = models.BooleanField(default = False)
           
    def __unicode__(self):
        return self.cas_user
    
    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"id":self.id})
     
    class Meta:
        managed = True
        db_table = 'users'