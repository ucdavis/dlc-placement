from django import forms
from .models import Languages


class LanguageForm(forms.ModelForm):
    class Meta:
        model = Languages
        fields = [
                  "name",
                  ]