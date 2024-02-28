from __future__ import unicode_literals
from django.db import models
from django.urls import reverse

# Create your models here.
class Languages(models.Model):
    id = models.AutoField(primary_key=True)  # AutoField
    name = models.CharField(max_length=32, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("language:detail", kwargs={"id":self.id})

    class Meta:
        managed = True
        db_table = 'languages'
        app_label = 'languages'