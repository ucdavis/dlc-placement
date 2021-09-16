from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models

# Create your models here.

class PlacementLevels(models.Model):
    id = models.IntegerField(primary_key=True) # AutoField?
    level = models.CharField(max_length=500)
    language_id = models.IntegerField()
    active = models.BooleanField(default = 1)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True) 
    
    def __unicode__(self):
        return self.level
    
    def get_absolute_url(self):
        return reverse("levels:detail", kwargs={"id":self.id})
    
    class Meta:
        managed = True
        app_label = 'levels'
        db_table = 'placement_levels'
        