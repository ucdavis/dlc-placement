from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models

# Create your models here.

class LanguagesUsers(models.Model):
    id = models.IntegerField(primary_key=True) # AutoField?
    language_id = models.IntegerField() # AutoField?
    user_id = models.IntegerField()# AutoField?

    def get_absolute_url(self):
        return reverse("languages_users:detail", kwargs={"id":self.id})
    
    def __unicode__(self):
        return self.id
     
    class Meta:
        managed = True
        app_label ='languages_users'
        db_table = 'languages_users'
        
class LanguagesUsersView(models.Model):
    id = models.IntegerField(primary_key=True) # AutoField?
    user_id = models.IntegerField()# AutoField?
    language_id = models.IntegerField() # AutoField?
    language_name = models.CharField(max_length = 32)
        
    def __unicode__(self):
        return self.language_name
     
    class Meta:
        managed = True
        app_label ='languages_users'
        db_table = 'languages_users_view'
