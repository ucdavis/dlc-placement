from django import forms
from languages.models import Languages
from functools import partial

DateInput = partial(forms.DateInput, {'class': 'datepicker'})

class LanguageForm(forms.Form):
    def __init__(self, *args, **kwargs):
        language_choices = kwargs.pop('language_choices')
        super(LanguageForm, self).__init__(*args, **kwargs)
        self.fields['language_id'].choices = language_choices  # @UndefinedVariable
             
    language_id = forms.ModelChoiceField(queryset=Languages.objects.all().order_by('name'), label = "Language", required=False, empty_label="All")  # @UndefinedVariable
# calendar fields
    
    start_date = forms.DateField(widget=DateInput())
    end_date = forms.DateField(widget=DateInput())
    
class EntryForm(forms.Form):
    def __init__(self, *args, **kwargs):
        language_choices = kwargs.pop('language_choices')
        super(EntryForm, self).__init__(*args, **kwargs)
        self.fields['language_id'].choices = language_choices  # @UndefinedVariable
             
    language_id = forms.ModelChoiceField(queryset=Languages.objects.all().order_by('name'), label = "Language", required=False, empty_label="All")  # @UndefinedVariable
# calendar fields
    
    created_at = forms.DateField(widget=DateInput(), label="Entered on or after")
    
class StudentForm(forms.Form):
    sid = forms.CharField(required = True, label="Student ID", widget=forms.Textarea(attrs={'cols': 20, 'rows': 10}))


class LastNameForm(forms.Form):
    last_name = forms.CharField(max_length=32, label="Last Name")
    
class EmailForm(forms.Form):
    email = forms.EmailField(required=True)