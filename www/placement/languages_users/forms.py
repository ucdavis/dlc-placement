from django import forms
from languages.models import Languages

#languages_queryset = Languages.objects.values_list("id","name").order_by('name')  # @UndefinedVariable
class LanguagesUsersForm(forms.Form):
    
    
    user_id = forms.CharField(widget=forms.HiddenInput())
    language_id = forms.MultipleChoiceField(required=False,
                                            label = "Languages", 
                                            widget=forms.CheckboxSelectMultiple, 
                                            )#choices=languages_queryset)
    user_id = forms.IntegerField()
    class Meta:

            fields = [
                      "language_id",
                      "user_id"
                      ]
            widgets = {'user_id': forms.HiddenInput()}