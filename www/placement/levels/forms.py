from django import forms
from .models import PlacementLevels


class LevelForm(forms.ModelForm):
#     level = forms.CharField(label= 'Level Name')
#     active = forms.BooleanField(label = 'Active', initial = True)
#    language_id = forms.IntegerField(required = True)  # @UndefinedVariable
    class Meta:
        model = PlacementLevels       
        fields = ["level","active","language_id"]
        widgets = {'language_id': forms.HiddenInput()}
        