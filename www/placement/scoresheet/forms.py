from django import forms
from .models import Scoresheet
from languages.models import Languages
from levels.models import PlacementLevels
from functools import partial


# # Choices for Language
queryset = Languages.objects.all().order_by('name')  # @UndefinedVariable
language_choices = [['','--------']]  
for data in queryset:
    language_choices.append([data.id,data.name])
     
# Choices for Levels    
queryset = PlacementLevels.objects.filter(active = 1).order_by('level')  # @UndefinedVariable
level_choices = [['','--------']]  
# for data in queryset:
#     level_choices.append([data.id,data.level])   
  
# JQuery datepicker     
DateInput = partial(forms.DateInput, {'class': 'datepicker'})
    

class ScoresheetForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        language_choices = kwargs.pop('language_choices')
        level_choices = kwargs.pop('level_choices')
        super(ScoresheetForm, self).__init__(*args, **kwargs)
        self.fields['language_id'].choices = language_choices  # @UndefinedVariable
        self.fields['placement_level_id'].choices = level_choices  # @UndefinedVariable


    sid = forms.CharField(label='Student ID', max_length=9, required = True)
    language_id = forms.ChoiceField(label='Language', choices=language_choices)  # @UndefinedVariable
    placement_level_id = forms.ChoiceField(choices=level_choices,label='Level') # @UndefinedVariable
    exam_date = forms.DateField(widget=DateInput())
    comments = forms.CharField(widget=forms.Textarea, label = "Score / Comments")
    needs_review = forms.BooleanField(initial=0, required=False)
    

    class Meta:
        model = Scoresheet       
        fields = [
                  "sid",
                  "first_name",
                  "last_name",
                  "email",
                  "tester_id",
                  "exam_date",
                  "language_id",
                  "placement_level_id",
                  "comments",
                  "needs_review",
                  "language_id"
                  ]
        widgets = {'tester_id': forms.HiddenInput(),
                   }

class BatchInputForm(forms.Form):
    placement_results = forms.CharField(widget=forms.Textarea)  