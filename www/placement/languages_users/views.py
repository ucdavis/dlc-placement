from django.shortcuts import render, redirect
from users.models import Users
from .models import LanguagesUsers
from .forms import LanguagesUsersForm
from languages.models import Languages
from django import forms
from django.http import HttpResponseRedirect
from django.contrib import messages

# Create your views here.
global title
title = "User Languages"

def languages_users_update(request, id=None):  # @ReservedAssignment
    if  'is_admin' in request.session: 
        instance = Users.objects.get(id=id)  # @UndefinedVariable
        # Load users languages and give them as initial parameters to the form    
        languages_queryset = Languages.objects.values_list("id","name").order_by('name')  # @UndefinedVariable
        languagesUser = LanguagesUsers.objects.filter(user_id = id).order_by('language_id')  # @UndefinedVariable 
        values = []
        for value in languagesUser:
            values.append(value.language_id)   
        user = Users.objects.get(id=id)  # @UndefinedVariable
        form =LanguagesUsersForm(request.POST or None, initial = {'user_id' : id, 'language_id' : values})
        form.fields['user_id'].widget = forms.HiddenInput()
        form.fields['language_id'] = forms.MultipleChoiceField(required=False,
                                            label = "Languages", 
                                            widget=forms.CheckboxSelectMultiple, 
                                            choices=languages_queryset)
        
        if request.POST.get('language_id'):
            LanguagesUsers.objects.filter(user_id = id).delete()  # @UndefinedVariable       
            for language_id in request.POST.getlist('language_id'):
                LanguagesUsers(user_id=id,language_id = int(language_id)).save()
            messages.success(request, "User Updated")     
            return HttpResponseRedirect(instance.get_absolute_url())  # @UndefinedVariable     
        
        context = {
                   "title" : title,
                   "subtitle" : "Languages for user: " + str(user),
                   "form" : form,
                   "languagesUser" : languagesUser,
                   "instance" : instance,
                   }
        return render(request,"languages_users_form.html",context)
    else:
        return redirect('home')
