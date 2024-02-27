from django.shortcuts import render, get_object_or_404, redirect
from .models import Users
from users.forms import UsersForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from languages_users.models import LanguagesUsers, LanguagesUsersView
from languages_users.forms import LanguagesUsersForm
from django import forms
import ldap
import json
from django.http.response import HttpResponse
import os

# Create your views here.

global title
title = "Users"


def validate_user(request):
# First function executed after CAS login
# Check if user exists in the placement database    
# Get the user's roles and active status
# If user is active save the user's variables in session and redirect to land page, else, the user is logged out
    cas_user = request.user
    user = Users.objects.filter(cas_user__exact=cas_user)  # @UndefinedVariable
    if(user):
        request.session['current_user'] = str(cas_user)
        
        for data in user:
            request.session['user_id'] = data.id
            if data.admin == 1:
                request.session['is_admin'] = True
            if data.advisor == 1:
                request.session['is_advisor'] = True
            if data.tester == 1:
                request.session['is_tester'] = True
            if data.active == 1:
                request.session['is_active'] = True                  
        if 'is_active' in request.session:              
            return redirect('home')
        else:
            return redirect("cas_ng_logout")


def users_list(request):
# Get and show  active users list to Administrators    
    if 'is_admin' in request.session: 
        queryset_users = Users.objects.filter(active__exact=1).order_by('cas_user')  # @UndefinedVariable
        context = {
                   "title" : title,
                   "subtitle" : "Active Users",
                   "queryset_users" : queryset_users,
                   }
        return render(request,"users_list.html", context)
    else:
        return redirect("home")
 

def users_inactive(request):
# Get and show  inactive users list to Administrators    
    if 'is_admin' in request.session: 
        queryset_users = Users.objects.filter(active__exact=0).order_by('cas_user')  # @UndefinedVariable
        context = {
                   "title" : title,
                   "subtitle" : "Inactive Users",
                   "queryset_users" : queryset_users,
                   }
        return render(request,"users_inactive.html", context)
    else:
        return redirect("home")
 

def users_detail(request, id=None):  # @ReservedAssignment
# Show user information and options to edit for Administrators
    if 'is_admin' in request.session: 
        user = get_object_or_404(Users,id=id)
    # Load users languages and give them as initial parameters to the form    
        languagesUser = LanguagesUsers.objects.filter(user_id = id).order_by('language_id')  # @UndefinedVariable 
        values = []
        for value in languagesUser:
            values.append(value.language_id)   
        formLanguages =LanguagesUsersForm(request.POST or None, initial = {'language_id' : values})
        formLanguages.fields['user_id'].widget = forms.HiddenInput()
        formLanguages.fields['language_id'].widget.attrs['disabled'] = True
        
        context = {
                   "title":title,
                   "subtitle" : "User Detail",
                   "user" : user,
                   "formLanguages" : formLanguages
                   }
        return render (request,"users_detail.html", context)
    else:
        return redirect("home")

def users_account(request):
# My Account web page, show current_user's information and languages. Read only.
    user = get_object_or_404(Users,id=request.session['user_id'])
    # Load users languages and give them as initial parameters to the form    
    languagesUser = LanguagesUsersView.objects.filter(user_id = user.id).order_by('language_name')  # @UndefinedVariable 
    values = []
    for value in languagesUser:
        values.append(value.language_id)   
    formLanguages =LanguagesUsersForm(request.POST or None, initial = {'language_id' : values})
    formLanguages.fields['user_id'].widget = forms.HiddenInput()
    formLanguages.fields['language_id'].widget.attrs['disabled'] = True

    context = {
               "title": "Account",
               "subtitle" : "My Account",
               "user" : user,
               "formLanguages" : formLanguages,
               "values" : values,
               "languagesUser" : languagesUser
               }
    return render (request,"users_account.html", context)


def users_create(request):
# Form to Crete new user for Administrators    
    if 'is_admin' in request.session: 
        form = UsersForm(request.POST or None)
        context = {
                   'title' : title,
                   'subtitle' : "New User",
                   'form' : form,
                   "clean_fields" : True
                   }
        if form.is_valid():
                new_user = form.save(commit=False)
                new_user.save()
                messages.success(request, "User Created : "+new_user.cas_user)
                return redirect("languages_users:edit", str(new_user.pk))
            
        return render(request,'users_form.html', context)
    
    else:
        return redirect("home")

def users_update(request, id=None):  # @ReservedAssignment
# Form to update user for Adminsitrators  
    if 'is_admin' in request.session: 
        instance = get_object_or_404(Users, id=id)
# TODO check if boolean field == 0 and change it to False so that can be rendered as unchecked checkbox when form is loaded               
        if instance.active==0 :
            instance.active = False
        if instance.admin==0:
            instance.admin=False
        if instance.tester==0:
            instance.tester = False
        if instance.advisor==0:
            instance.advisor=False             
        
        form = UsersForm(request.POST or None , instance = instance)
# Validate form and save the data
        if form.is_valid():
            instance = form.save(commit = False)
            instance.save()
            messages.success(request, "User Updated")
            return HttpResponseRedirect(instance.get_absolute_url())  # @UndefinedVariable       
        context = {
                   "title" : "User Details",
                   "subtitle" : "Update User : ",
                   "form" : form,
                   "instance" : instance, 
                   "clean_fields" : "False"           
                   }
        return render(request, "users_form.html", context)
    
    else:
        return redirect("home")
    

def GetUserLDAP( request=False, uid=None ):
    # LDAP query      
    server = os.environ["LDAP_SERVER"]
    base = os.environ["LDAP_BASE"]
    username = os.environ['LDAP_USER']
    password = os.environ["LDAP_PASS"]
    searchFilter = "(uid="+str(uid)+")"
 
    try:                 
        l = ldap.initialize(server)
        l.protocol_version = ldap.VERSION3
        l.simple_bind_s(username,password)          
        result= l.search_s(base, ldap.SCOPE_SUBTREE, searchFilter)
        user_data={}
        for data in result:
            user_data['first_name']=data[1]['givenName'][0]
            user_data['last_name']=data[1]['sn'][0]
            user_data['email']=data[1]['mail'][0]
            user_data['department']=data[1]['ou'][0]
        return HttpResponse(json.dumps(user_data) , content_type="application/json")
         
    except ldap.LDAPError as error:
        print('Problems with ldap',error)
        return False
