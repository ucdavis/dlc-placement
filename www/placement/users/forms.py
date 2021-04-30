from django import forms
from .models import Users



class UsersForm(forms.ModelForm):
    cas_user = forms.CharField(label='Username (Kerberos)', max_length=25)
    first_name = forms.CharField(label='First Name', max_length=50)
    last_name = forms.CharField(label='Last Name', max_length=50)
    department = forms.CharField(label='Department', max_length=255)
    email = forms.EmailField( max_length=255)
    advisor = forms.CheckboxInput()
    tester = forms.CheckboxInput()
    admin = forms.CheckboxInput()
    active = forms.CheckboxInput()

    class Meta:
        model = Users
        fields = [
                  "cas_user",
                  "first_name",
                  "last_name",
                  "department",
                  "email",
                  "advisor",
                  "tester",
                  "admin",
                  "active"
                  ]