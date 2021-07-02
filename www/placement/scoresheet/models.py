from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.fields import CharField

# Create your models here.
class Scoresheet(models.Model):
    id = models.AutoField(primary_key=True) # AutoField?
    sid = models.CharField(max_length=16, null=False, blank=True, default='')
    first_name = models.CharField(max_length=32, blank=True, default='')
    last_name = models.CharField(max_length=32,blank=True, default='')
    email = models.EmailField()
    comments = models.TextField(max_length=255, null=True, blank=True, default='')
    tester_id = models.IntegerField()
    exam_date = models.DateField()
    language_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    placement_level_id = models.IntegerField()
    needs_review = models.BooleanField(default=0)
     
    def __unicode__(self):
        return self.sid
    
    def get_absolute_url(self):
        return reverse("scoresheet:detail", kwargs={"id":self.id})
     
    class Meta:
        managed = True
        app_label ='scoresheet'
        db_table = 'scoresheets'
        


class ScoresheetView(models.Model):
    id = models.IntegerField(primary_key=True) # AutoField?
    sid = models.CharField(max_length=16, null=False, blank=True, default='')
    first_name = models.CharField(max_length=32, blank=True, default='')
    last_name = models.CharField(max_length=32,blank=True, default='')
    email = models.EmailField()
    comments = models.TextField(max_length=255, null=True, blank=True, default='')
    user_id = models.IntegerField()
    cas_user = models.CharField(max_length=255)
    level_id = models.IntegerField()
    level = CharField(max_length=500)
    exam_date = models.DateField()
    language_id = models.IntegerField()
    language_name = models.CharField(max_length=255, null=True)
    needs_review = models.BooleanField(default=0)
     
    def __unicode__(self):
        return self.sid
     
    class Meta:
        managed = True
        app_label ='scoresheet'
        db_table = 'scoresheets_view'