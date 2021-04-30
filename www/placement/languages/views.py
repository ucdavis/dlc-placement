from django.shortcuts import render, get_object_or_404, redirect
from .models import Languages
#from levels.models import PlacementLevels
from django.http import HttpResponseRedirect
from .forms import LanguageForm
from django.contrib import messages

# Create your views here.
global title
title = "Languages"


def language_list(request):
    if  'is_admin' in request.session: 
        queryset_list = Languages.objects.all().order_by('name')  # @UndefinedVariable
        context = {
                   "title" : title,
                   "subtitle" : "List",
                   "queryset_list" : queryset_list,
                   }
        return render(request,"language_list.html", context)
    else:
        return redirect('home')


def language_detail(request, id=None):  # @ReservedAssignment
    instance = get_object_or_404(Languages, id=id)
    context = {
               "title" : title,
               "subtitle" : "Detail",
               "instance" : instance,
               }   
    return render(request,"language_detail.html",context)


def language_create(request):
    if  'is_admin' in request.session: 
        form = LanguageForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, "Language successfully created")
            return redirect("language:list")
        
        context = {
                   "title" : title,
                   "subtitle" : "New",
                   "form" : form
                   }
        return render(request,"language_form.html",context)
    else:
        return redirect('home')


def language_update(request, id=None):  # @ReservedAssignment
    if  'is_admin' in request.session:     
        instance = get_object_or_404(Languages, id=id)
        form = LanguageForm(request.POST or None, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, "Successfully Updated")
            return HttpResponseRedirect(instance.get_absolute_url())  # @UndefinedVariable
        context = {
                   "title" : title,
                   "subtitle" : "Edit",
                   "instance" : instance,
                   "form" : form
                   }   
        return render(request,"language_form.html",context)
    else:
        return redirect('home')


def language_delete(request, id=None):  # @ReservedAssignment
    if  'is_admin' in request.session:  
        instance = get_object_or_404(Languages, id=id)
        instance.delete()
    #     messages.success(request, "Successfully Deleted")
        return redirect("language:list")
    else:
        return redirect('home')

 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
    