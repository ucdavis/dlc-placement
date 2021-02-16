from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .models import PlacementLevels
from languages.models import Languages
from .forms import LevelForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

global title
title = "Levels"

def level_list(request, id=None):  # @ReservedAssignment
    if  'is_admin' in request.session: 
        query_level_list = PlacementLevels.objects.filter(language_id=id).order_by('-active','level')  # @UndefinedVariable 
        query_language = Languages.objects.get(id=id)  # @UndefinedVariable  
        total_rows = query_level_list.count()
        for level in query_level_list:
            if(level.active == 1):
                level.active = 'Active'
            else:
                level.active = 'Inactive'      
             
    #PAGINATOR      
        paginator = Paginator(query_level_list, 50) # Show n records per page
        page_request_var = "page"
        page = request.GET.get(page_request_var)
        try:
            level_list = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            level_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            level_list = paginator.page(paginator.num_pages)     
            
                       
        content = {
                   "title" : title,
                   "subtitle" : "Levels",
                   "level_list" : level_list,
                   "query_language" : query_language,
                   "language_id" : id,
                   "page_request_var" : page_request_var,
                   "total_rows" : total_rows 
                   }
        
        return render(request,"level_list.html", content)
    else:
        return redirect('home')


def level_create(request, id=None):  # @ReservedAssignment
    if  'is_admin' in request.session:     
        language = Languages.objects.get(id=id)  # @UndefinedVariable  
        form =LevelForm(request.POST or None, initial = {'language_id':id})
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return redirect ("/levels/"+id)
        
        context = {
                   "title" : title,
                   "subtitle" : "New Level",
                   "form" : form,
                   "language" : language,
                   "language_id" : id,
                   }
        return render(request,"level_form.html",context)
    else:
        return redirect('home')

def level_detail(request, id=None):  # @ReservedAssignment
    instance = get_object_or_404(PlacementLevels,id=id)
    language = Languages.objects.get(id=instance.language_id)  # @UndefinedVariable
    context = {
               "title" : title,
               "subtitle" : "Level Detail",
               "instance" : instance,
               "language" : language,
               }    
    return render(request,"level_detail.html",context)

def level_update(request, id=None):  # @ReservedAssignment
    if  'is_admin' in request.session:   
        instance = get_object_or_404(PlacementLevels, id=id)
        if (instance.active == 1):
            instance.active = True
        else:
            instance.active = False    
        language = Languages.objects.get(id=instance.language_id)  # @UndefinedVariable
        form = LevelForm(request.POST or None, instance = instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request,"Successfully Updated")
            return HttpResponseRedirect(instance.get_absolute_url())  # @UndefinedVariable
        context = {
                   "title" : title,
                   "subtitle" : "Edit Level",
                   "instance" : instance,
                   "language" : language,
                   "language_id" : instance.language_id,
                   "form" : form
                   }
        return render(request,"level_form.html",context)
    else:
        return redirect('home')

