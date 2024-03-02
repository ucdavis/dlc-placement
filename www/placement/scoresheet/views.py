from django.shortcuts import render, get_object_or_404, redirect
from .forms import ScoresheetForm, BatchInputForm
from users.models import Users
from languages.models import Languages
from scoresheet.models import Scoresheet, ScoresheetView
from levels.models import PlacementLevels
from languages_users.models import LanguagesUsersView
from datetime import datetime
from django.db.models import Q
from django import forms
import csv
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from django.contrib import messages
from django.template import loader, Context
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import os
import oracledb
from utils.iam_client import IAMClient


global title
title = "Scoresheets"

def scoresheet_list(request):  # @ReservedAssignment
# Get variables from form    
    language_id_var =request.GET.get("language_id")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    created_at = request.GET.get("created_at")
    last_name = request.GET.get("last_name")
    sid = request.GET.get('sid')

# SEARCH BY LANGUAGE
# if user is tester search only for assigned languages
    language_ids= LanguagesUsersView.objects.values('language_id').filter(user_id__exact=request.session['user_id'])# @UndefinedVariable
    if ('is_tester' in request.session) and ('is_admin' not in request.session):             
        scoresheet_list = ScoresheetView.objects.filter(language_id__in=language_ids).order_by( '-exam_date')  # @UndefinedVariable
    elif('is_admin' in request.session) or ('is_advisor' in request.session):    
        scoresheet_list = ScoresheetView.objects.all().order_by('-exam_date')  # @UndefinedVariable
        
# search by period of time and language  
    if (language_id_var and start_date and end_date ):
        scoresheet_list = ScoresheetView.objects.filter(  # @UndefinedVariable
                                                    Q(language_id__exact = language_id_var)&
                                                    Q(exam_date__range=[start_date, end_date]) 
                                                    )
    elif (language_id_var and created_at):
        if ('is_tester' in request.session) and ('is_admin' not in request.session):     
            scoresheet_list = ScoresheetView.objects.filter(language_id__exact=language_id_var, created_at__gte=created_at).order_by( '-created_at')  # @UndefinedVariable
        elif('is_admin' in request.session) or ('is_advisor' in request.session):    
            scoresheet_list = ScoresheetView.objects.filter(language_id__exact=language_id_var, created_at__gte=created_at).order_by( '-created_at')  
# search all from language                
    elif (language_id_var):
        scoresheet_list = ScoresheetView.objects.filter( language_id__exact = language_id_var)  # @UndefinedVariable
# search for all in DB  for period      
    elif (language_id_var=='' and start_date and end_date ):     
        if ('is_tester' in request.session) and ('is_admin' not in request.session):     
            scoresheet_list = ScoresheetView.objects.filter(language_id__in=language_ids, exam_date__range=[start_date, end_date]).order_by( '-exam_date')  # @UndefinedVariable
        elif('is_admin' in request.session) or ('is_advisor' in request.session):    
            scoresheet_list = ScoresheetView.objects.filter(exam_date__range=[start_date, end_date]).order_by( '-exam_date')    # @UndefinedVariable
 # search for scoresheet created_at
    elif (language_id_var=='' and created_at):
        if ('is_tester' in request.session) and ('is_admin' not in request.session):     
            scoresheet_list = ScoresheetView.objects.filter(language_id__in=language_ids, created_at__gte=created_at).order_by( '-created_at')  # @UndefinedVariable
        elif('is_admin' in request.session) or ('is_advisor' in request.session):    
            scoresheet_list = ScoresheetView.objects.filter(created_at__gte=created_at).order_by( '-created_at')    # @UndefinedVariable
# search all for student last name     
    elif ( last_name ):
        if ('is_tester' in request.session) and ('is_admin' not in request.session):             
            scoresheet_list = ScoresheetView.objects.filter(language_id__in=language_ids, last_name__iexact=last_name).order_by('last_name', 'first_name')  # @UndefinedVariable
        elif('is_admin' in request.session) or ('is_advisor' in request.session):    
            scoresheet_list = ScoresheetView.objects.filter(last_name__iexact=last_name).order_by('last_name', 'first_name')  # @UndefinedVariable
        
# Search for single or multiplw Student ID sid        
    elif ( sid ):
        ids = sid.replace('\n', ' ').replace('\r', '').split(" ")
        scoresheet_list = ScoresheetView.objects.filter(sid__in=ids).exclude( sid__isnull= True).exclude(sid__exact='').order_by('sid')  # @UndefinedVariable
        total_rows=scoresheet_list.count() 
        
    if request.GET.get('csv'):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Placement_Report.csv"'
     
        writer = csv.writer(response)
        writer.writerow(['Student ID', 'First Name', 'Last Name', 'E-mail', 'Language', 'Placement', 'Exam Date', 'PP Entered Date', 'Tester', 'Comments', 'Needs Review'])
        for scoresheet in scoresheet_list:
            writer.writerow([scoresheet.sid,
                             scoresheet.first_name,
                             scoresheet.last_name,
                             scoresheet.email,
                             scoresheet.language_name,
                             scoresheet.level,
                             scoresheet.exam_date,
                             scoresheet.created_at,
                             scoresheet.cas_user,
                             scoresheet.comments,
                             scoresheet.needs_review])
        return response
     
        context = {
               "title" : title,
               "subtitle" : "Report",
               "scoresheet_list" : scoresheet_list,
               "total_rows" : total_rows
               }
    
        return render(request,"scoresheet_list.html", context)            
       
  
#PAGINATOR
    paginator = Paginator(scoresheet_list, 25) # Show n records per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        scoresheet_list_pag = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        scoresheet_list_pag = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        scoresheet_list_pag = paginator.page(paginator.num_pages)    
         
    total_rows=scoresheet_list.count()
           
    #Context to render
    context = {
               "title" : title,
               "subtitle" : "Report",
               "scoresheet_list" : scoresheet_list_pag,
               "page_request_var" : page_request_var,
               "total_rows" : total_rows
               }
    
    return render(request,"scoresheet_list.html", context)

def scoresheet_create(request):
    if ('is_admin' in request.session) or ('is_tester' in request.session):
        user_id= request.session['user_id']
        level_choices = [['','--------']]
        queryset_id_languages= Languages.objects.values('id')  # @UndefinedVariable              
        queryset_levels = PlacementLevels.objects.filter(active = 1, language_id__in=queryset_id_languages) # @UndefinedVariable
        for levels in queryset_levels:
            level_choices.append([levels.id,levels.level])  
# Get languages for user            
        if ('is_tester' in request.session) and ('is_admin' not in request.session):
            queryset_languages_user = LanguagesUsersView.objects.filter(user_id__exact=user_id).order_by('language_name')  # @UndefinedVariable
            language_choices = [['','--------']]  
            for data in queryset_languages_user:
                language_choices.append([data.language_id,data.language_name])                             
            form =ScoresheetForm(request.POST or None,language_choices=language_choices, level_choices=level_choices, initial ={'tester_id':user_id})
            form.fields['needs_review'].widget = forms.HiddenInput()
        else:
            queryset_languages = Languages.objects.all().order_by('name')  # @UndefinedVariable
            language_choices = [['','--------']]            
            for data in queryset_languages:
                language_choices.append([data.id,data.name])      
            form =ScoresheetForm(request.POST or None,language_choices=language_choices, level_choices=level_choices, initial ={'tester_id':user_id})
            form.fields['needs_review'].widget = forms.HiddenInput()
# Validate the form and SAVE the scoresheet
        if form.is_valid():             
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, "Scoresheet Created : "+instance.sid)
            
# Prepare info for confirmation Email
            language = Languages.objects.get(id = form.cleaned_data['language_id'])  # @UndefinedVariable
            placement_level = PlacementLevels.objects.get(id = form.cleaned_data['placement_level_id'])  # @UndefinedVariable
# Check for duplicated Scoresheets            
            duplicated_checker = ScoresheetView.objects.filter(# @UndefinedVariable
                                                         Q(sid__exact = instance.sid)&
                                                         Q(level_id = instance.placement_level_id)
                                                         )
            context = {
                       "full_name" : form.cleaned_data['first_name']+" "+form.cleaned_data['last_name'],
                       "first_name" : form.cleaned_data['first_name'],
                       "last_name" : form.cleaned_data['last_name'],
                       "language" : language,
                       "sid" : form.cleaned_data['sid'],                       
                       "exam_date" : form.cleaned_data['exam_date'],
                       "email" : form.cleaned_data['email'],
                       "placement_level" : placement_level,
                       "queryset_checker" : duplicated_checker           
                       }
                        
# If scoresheet is not duplicated send confirmation email to student
            EMAIL_FAIL_SILENTLY=False
            if(os.environ['EMAIL_FAIL_SILENTLY'] == "True"):
                EMAIL_FAIL_SILENTLY=True

            if (duplicated_checker.count() == 1):      
                to_email = [form.cleaned_data.get('email')]
                email_html_template = loader.get_template('student_email.html')
                email_txt_template = loader.get_template('student_email.txt')
                html_content = email_html_template.render(context)
                text_content = email_txt_template.render(context)          
                subject = "Message from Placement"
                from_email = settings.EMAIL_FROM
                message = EmailMultiAlternatives(subject, text_content, from_email, to_email)
                message.attach_alternative(html_content, 'text/html')
                message.send(fail_silently=EMAIL_FAIL_SILENTLY)
            
# If duplicated placement send notification to Admin list

            if (duplicated_checker.count() >= 2):
                to_email = os.environ['ADMIN_EMAIL_LIST'].split(';')
                email_html_template = loader.get_template('duplicated_placement_email.html')
                email_txt_template = loader.get_template('duplicated_placement_email.txt')
                html_content = email_html_template.render(context)
                text_content = email_txt_template.render(context)          
                subject = "Duplicated Placement"
                from_email = settings.EMAIL_FROM
                message = EmailMultiAlternatives(subject, text_content, from_email, to_email)
                message.attach_alternative(html_content, 'text/html')
                message.send(fail_silently=EMAIL_FAIL_SILENTLY)
                messages.error(request, "DUPLICATED Scoresheet for student ID "+str(instance.sid)+". Created and sent to administrators for review")         
            
# If student info was manually entered, send notification to Admin list
            if (form.cleaned_data['needs_review']):
                to_email = os.environ['ADMIN_EMAIL_LIST'].split(';')
                email_html_template = loader.get_template('needs_review_email.html')
                email_txt_template = loader.get_template('needs_review_email.txt')
                html_content = email_html_template.render(context)
                text_content = email_txt_template.render(context)          
                subject = "Placement Manually Entered"
                from_email = settings.EMAIL_FROM
                message = EmailMultiAlternatives(subject, text_content, from_email, to_email)
                message.attach_alternative(html_content, 'text/html')
                message.send(fail_silently = EMAIL_FAIL_SILENTLY) 
                messages.error(request, "NOT FOUND. Student ID "+str(instance.sid)+". Information was manually entered and and sent to administrators for review") 
                
# Redirect to new scoresheet's detail page                              
            return HttpResponseRedirect(instance.get_absolute_url())  # @UndefinedVariable

# Initialize the form when page is loded
        context = {
                   "title" : title,
                   "subtitle" : "New Scoresheet",
                   "form" : form,
                   "user_id" : user_id,
                   "clean_fields" : "True"   
                   }
        return render(request,"scoresheet_form.html",context)
# If user is not admin or tester, redirect to home page
    else:
        return redirect('home')

def scoresheet_bulk_input(request):
    if ('is_admin' in request.session):
        form = BatchInputForm(request.GET or None)
        if form.is_valid():

# Create a .txt file with the tab-separated data entered in the form's text area
            placement_results = form.cleaned_data['placement_results']
            path = settings.BASE_DIR+'/temp/data.txt'
            
            with open(path,'w') as txt_file:
                for records in placement_results:
                    txt_file.write(records)
            txt_file.closed        
# Open the file and save the data into an array                   
            with open(path) as txt_file:
                reader = csv.reader(txt_file, delimiter="\t")
                data = list(reader)

                
# For each row in file:
# Check for blank columns and required fields
                max_rows = 5
                for row in data:              
                    if len(row) < max_rows:
                        messages.error(request,"BLANK COLUMNS. Please provide all the required fields.")
                        return(redirect("scoresheet:bulk_input"))
 
                    elif not(row[0]) or not(row[1]) or not(row[2]) or not(row[3]) or not(row[4]):
                        messages.error(request,"BLANK COLUMNS. Please provide all the required fields.")
                        return(redirect("scoresheet:bulk_input"))
# Check for date format in scoresheet_data (YYY-MM-DD)
                for row in data: 
                    validation = validate_date(row[4])
                    if validation == False: 
                        messages.error(request,"WRONG DATE FORMAT. Date must be YYYY-MM-DD formatted.")
                        return(redirect("scoresheet:bulk_input")) 
                                          
# If data is valid                     
# store data in scoresheet array              
                for row in data:                 
                    scoresheet_data= {}                    
                    if (len(row)==5):                                           
                        scoresheet_data['comments'] = "Bulk Input"
                    
                    scoresheet_data['id'] = row[0]
                    scoresheet_data['last_name'] = row[1]
                    scoresheet_data['language'] = row[2]   
                    scoresheet_data['placement'] = row[3]
                    scoresheet_data['exam_date'] = row[4]
                    if (len(row) == 6):
                        if row[5] in (None, ''):             
                            scoresheet_data['comments'] = "Bulk Input"
                        else:
                            scoresheet_data['comments'] = row[5]
   
                    language_id = GetLanguageId(language_name=scoresheet_data['language'])
                    level_id = GetLevelId(level_name=scoresheet_data['placement'])
 
                 
                    # Match student ID and last_name in Banner. If student is valid add the information to the scoresheet array
                    last_name = scoresheet_data['last_name']

                    is_id_sid = scoresheet_data['id'].isdigit()

                    if is_id_sid:
                        student_id = scoresheet_data['id']
                        student_email = ''
                        student_data = GetStudentBanner(sid=student_id, formatted='dictionary')
                        if 'email' in student_data:
                            student_email = student_data['email']
                        # if email is null looks for it in IAM
                        if(student_email ==''):
                            student_email = GetEmailIAM(sid=student_id)
                    else:
                        student_id = ''
                        student_email = scoresheet_data['id']
                        student_data = GetStudentInfoFromEmail(email=student_email, formatted='dictionary')
                        if 'sid' in student_data:
                            student_id = student_data['sid']


                    if student_email != '' and student_id != '':
                        scoresheet_data['first_name']=student_data['first_name']
                        scoresheet_data['last_name']=student_data['last_name']
                        if (student_data ['last_name'].lower() != last_name.lower()):
                            if is_id_sid:
                                messages.error(request, "NOT MATCH. Student ID and Last Name do not match for sid: "+student_id)
                            else:
                                messages.error(request, "NOT MATCH. Email and Last Name do not match for email: "+student_email)
                        else:
                            scoresheet_data['email']=student_email
                            scoresheet_data['language_id'] = language_id
                            scoresheet_data['placement_level_id'] = level_id
                            # If the student is valid Save the scoresheet
                            instance = Scoresheet(sid = student_id,
                                       first_name = scoresheet_data['first_name'],
                                       last_name = scoresheet_data['last_name'],
                                       email = student_email,
                                       comments = scoresheet_data['comments'],
                                       tester_id = request.session['user_id'],
                                       exam_date = scoresheet_data['exam_date'] ,
                                       language_id = scoresheet_data['language_id'],
                                       placement_level_id = scoresheet_data['placement_level_id']
                                       )
                            instance.save()
                            if is_id_sid:
                                log_message = "CREATED. Scoresheet Student ID : "+ str(instance.sid)+". "
                            else:
                                log_message = "CREATED. Scoresheet Student Email : "+ instance.email+". "

                            # After creating the scoresheet, check if it was duplicated
                            duplicated_checker = ScoresheetView.objects.filter(# @UndefinedVariable
                                                         Q(sid__exact = instance.sid)&
                                                         Q(level_id = instance.placement_level_id)
                                                         )

                            # Create context for Emails
                            language = Languages.objects.get(id = instance.language_id)  # @UndefinedVariable
                            placement_level = PlacementLevels.objects.get(id = instance.placement_level_id)  # @UndefinedVariable
                            EMAIL_FAIL_SILENTLY=False
                            if(os.environ['EMAIL_FAIL_SILENTLY'] == "True"):
                                EMAIL_FAIL_SILENTLY=True

                            context = {
                                       "full_name" : instance.first_name + " " +instance.last_name,
                                       "first_name" : instance.first_name,
                                       "last_name" : instance.last_name,
                                       "language" : language,
                                       "sid" : instance.sid,
                                       "exam_date" : instance.exam_date,
                                       "email" : instance.email,
                                       "placement_level" : placement_level,
                                       "queryset_checker" : duplicated_checker
                                       }

                            # If scoresheet was duplicated add a warning to message and send email to administrators
                            if (duplicated_checker.count() >= 2):
                                to_email = os.environ['ADMIN_EMAIL_LIST'].split(';')
                                email_html_template = loader.get_template('duplicated_placement_email.html')
                                email_txt_template = loader.get_template('duplicated_placement_email.txt')
                                html_content = email_html_template.render(context)
                                text_content = email_txt_template.render(context)
                                subject = "Duplicated Placement"
                                from_email = settings.EMAIL_FROM
                                message = EmailMultiAlternatives(subject, text_content, from_email, to_email)
                                message.attach_alternative(html_content, 'text/html')
                                message.send(fail_silently = EMAIL_FAIL_SILENTLY)
                                log_message +=  "DUPLICATED scoresheet sent to administrator for review."

                            # If scoresheet was not duplicated send confirmation Email to student
                            elif (duplicated_checker.count() == 1):
                                to_email = [instance.email]
                                email_html_template = loader.get_template('student_email.html')
                                email_txt_template = loader.get_template('student_email.txt')
                                html_content = email_html_template.render(context)
                                text_content = email_txt_template.render(context)
                                subject = "Message from Placement"
                                from_email = settings.EMAIL_FROM
                                message = EmailMultiAlternatives(subject, text_content, from_email, to_email)
                                message.attach_alternative(html_content, 'text/html')
                                message.send(fail_silently = EMAIL_FAIL_SILENTLY)
                            # Diplay message
                            if "DUPLICATED" in log_message:
                                messages.warning(request, log_message)
                            else:
                                messages.success(request, log_message)
                                                  
                                    
                    # If Student ID was not found in LDAP display error message and do nothing. Must be entered via single scoresheet
                    elif student_id == '':
                            messages.error(request, "NOT FOUND. Email : "+student_email)
                    else:  
                            messages.error(request, "NO EMAIL. No email registered for sid: "+student_id)
                txt_file.closed
                os.remove(settings.BASE_DIR+'/temp/data.txt')
                                                    
        context={
                'form' : form
                }    
                   
        return render (request, "bulk_input.html", context )
    else:
        return redirect ("home")
 
def validate_date(d):
    try:
        datetime.strptime(d, '%Y-%m-%d')
        return True
    except ValueError:
        return False
        
def get_levels(request, language_id):  
    levels= PlacementLevels.objects.filter(  # @UndefinedVariable
                                           Q(language_id=language_id)&
                                           Q(active =  1)
                                           )
    return HttpResponse(json.dumps([dict(item) for item in levels.values('pk','level')]) , content_type="application/json")
        
def scoresheet_detail(request, id=None):  # @ReservedAssignment
    scoresheet = Scoresheet.objects.get(id=id)  # @UndefinedVariable
    language = Languages.objects.get(id=scoresheet.language_id)  # @UndefinedVariable
    placement = PlacementLevels.objects.get(id=scoresheet.placement_level_id)  # @UndefinedVariable
    tester = Users.objects.get(id=scoresheet.tester_id)  # @UndefinedVariable
    
    if (request.GET.get('email')):
        context = {
                       "full_name" : scoresheet.first_name +" "+ scoresheet.last_name,
                       "first_name" : scoresheet.first_name,
                       "last_name" : scoresheet.last_name,
                       "language" : language,
                       "sid" : scoresheet.sid,                       
                       "exam_date" : scoresheet.exam_date,
                       "email" : scoresheet.email,
                       "placement_level" : placement,                   
                       }
    # Send Email to student
        EMAIL_FAIL_SILENTLY=False
        if(os.environ['EMAIL_FAIL_SILENTLY'] == "True"):
            EMAIL_FAIL_SILENTLY=True
        to_email = scoresheet.email
        email_html_template = loader.get_template('student_email.html')
        email_txt_template = loader.get_template('student_email.txt')
        html_content = email_html_template.render(context)
        text_content = email_txt_template.render(context)          
        subject = "Message from Placement"
        from_email = settings.EMAIL_FROM
        message = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        message.attach_alternative(html_content, 'text/html')
        message.send(fail_silently = EMAIL_FAIL_SILENTLY)
        messages.success(request, "Email successfully sent to student.")
        
    context = {
               "title" : title,
               "subtitle" : "Scoresheet Detail",
               "scoresheet" : scoresheet,
               "language" : language,
               "placement" : placement,
               "tester" : tester
               }    
    return render(request,"scoresheet_detail.html",context)
 
def scoresheet_update(request, id=None):  # @ReservedAssignment
    if ('is_admin' in request.session) or ('is_tester' in request.session):
        instance = get_object_or_404(Scoresheet, id=id)
        checked = False
        if(instance.needs_review == 1):
            checked = True            
        language = Languages.objects.get(id=instance.language_id)  # @UndefinedVariables
        user_id= request.session['user_id']
        # Get languages and level for user
        if ('is_tester' in request.session) and ('is_admin' not in request.session):
            queryset_languages_user = LanguagesUsersView.objects.filter(user_id__exact=user_id).order_by('language_name')  # @UndefinedVariable
            language_choices = []  
            for data in queryset_languages_user:
                language_choices.append([data.language_id,data.language_name])
            
            queryset_levels = PlacementLevels.objects.filter(active = 1, language_id=instance.language_id).order_by('level')  # @UndefinedVariable
            level_choices = []  
            for levels in queryset_levels:
                level_choices.append([levels.id,levels.level])        
                
            form =ScoresheetForm(request.POST or None,language_choices=language_choices, level_choices = level_choices, instance=instance, initial ={'needs_review':checked})
            form.fields['needs_review'].widget = forms.HiddenInput()
        else:
            queryset = Languages.objects.all().order_by('name')  # @UndefinedVariable
            language_choices = [] 
            for data in queryset:
                language_choices.append([data.id,data.name])
            
            level_choices = []
            queryset_levels = PlacementLevels.objects.filter(active = 1, language_id=instance.language_id) # @UndefinedVariable             
            for levels in queryset_levels:
                level_choices.append([levels.id,levels.level]) 
                
            form =ScoresheetForm(request.POST or None,language_choices=language_choices,instance=instance, level_choices=level_choices, initial ={'needs_review':checked})

                
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request,"Scoresheet Successfully Updated")
            return HttpResponseRedirect(instance.get_absolute_url())  # @UndefinedVariable
        context = {
                   "title" : title,
                   "subtitle" : "Edit Level",
                   "instance" : instance,
                   "language" : language,
                   "language_id" : instance.language_id,
                   "form" : form,
                   "clean_fields" : "False" 
                   }
        return render(request,"scoresheet_form.html",context)
    else:
        return redirect('home')

def scoresheet_delete(request, id, template_name='scoresheet_confirm_delete.html'):  # @ReservedAssignment
    if ('is_admin' in request.session) or ('is_tester' in request.session):
        scoresheet = get_object_or_404(Scoresheet, pk=id)    
        if request.method=='POST':
            scoresheet.delete()
            messages.success(request, "Scoresheet deleted")
            return redirect('home')
        return render(request, template_name, {'object':scoresheet})
    else:
        return redirect('home')
    
def GetEmailIAM(request=False, sid=None):
    iam = IAMClient()
    return iam.get_email_by_student_id(sid=sid)

def GetStudentBanner(request=False, sid=None, formatted=None):
    # Build connection string
    user = os.environ["BANNER_USER"]
    pswd = os.environ["BANNER_PASS"]
    host = os.environ["BANNER_HOST"]
    port = os.environ["BANNER_PORT"]
    db = os.environ["BANNER_DB"]

    # Connect to Oracle
    oracledb.init_oracle_client() # thick mode
    dsn = oracledb.makedsn (host, port, db)  # @UndefinedVariable
    con = oracledb.connect(user=user, password=pswd, dsn=dsn)  # @UndefinedVariable
    cur = con.cursor()
    if (con):
        cur.prepare("SELECT SPRIDEN_FIRST_NAME, SPRIDEN_LAST_NAME FROM SPRIDEN WHERE SPRIDEN_ID = :sid AND SPRIDEN_CHANGE_IND IS NULL")
        cur.execute(None, {'sid': sid})
        result1 = cur.fetchall()

        cur.prepare("SELECT SPRIDEN_PIDM FROM SPRIDEN WHERE SPRIDEN_ID = :sid AND SPRIDEN_CHANGE_IND IS NULL")
        cur.execute(None, {'sid': sid})
        result2 = cur.fetchall()
        if result2:
            pidm = str(result2[0][0])
            cur.prepare("SELECT GOREMAL_EMAIL_ADDRESS FROM GOREMAL WHERE GOREMAL_PIDM = :pidm AND GOREMAL_EMAL_CODE = 'UCD'")
            cur.execute(None, {'pidm': pidm})
            result3 = cur.fetchall()
            email = ""
            if result3:
                email = result3[0][0]
            else:
                email = GetEmailIAM(sid=sid)
        else:
            pidm = ""    
      
        if (formatted=='json'):
            student_data=[]
            if (pidm==""):
                return HttpResponse(json.dumps(student_data) , content_type="application/json")
            else:
                for data in result1:
                    student_data.append( [data[0],data[1], email ] )
                return HttpResponse(json.dumps(student_data) , content_type="application/json")
        elif (formatted=='dictionary'):
            student_data={}
            for data in result1:
                student_data['first_name']=data[0]
                student_data['last_name']=data[1]
                student_data['email']=email      
            return student_data 

    else:
        return False
            
def GetStudentInfoFromEmail(request=False, email=None, formatted='json'):
    if email:
        user = os.environ["BANNER_USER"]
        pswd = os.environ["BANNER_PASS"]
        host = os.environ["BANNER_HOST"]
        port = os.environ["BANNER_PORT"]
        db = os.environ["BANNER_DB"]

        oracledb.init_oracle_client() # thick mode
        dsn = oracledb.makedsn (host, port, db)
        con = oracledb.connect(user=user, password=pswd, dsn=dsn)

        cur = con.cursor()
        if (con):
            cur.prepare("SELECT GOREMAL_PIDM FROM GOREMAL WHERE GOREMAL_EMAIL_ADDRESS = :email AND GOREMAL_EMAL_CODE = 'UCD'")
            cur.execute(None, {'email': email})
            pidm_res = cur.fetchall()
            if pidm_res:
                pidm = str(pidm_res[0][0])
                cur.prepare("SELECT SPRIDEN_FIRST_NAME, SPRIDEN_LAST_NAME, SPRIDEN_ID FROM SPRIDEN WHERE SPRIDEN_PIDM = :pidm AND SPRIDEN_CHANGE_IND IS NULL")
                cur.execute(None, {'pidm': pidm})
                info_res = cur.fetchall()
                if info_res:
                    if formatted == 'json':
                        student_data=[[info_res[0][0], info_res[0][1], info_res[0][2]]]
                        return HttpResponse(json.dumps(student_data) , content_type="application/json")
                    else:
                        student_data = {
                            'first_name': info_res[0][0],
                            'last_name': info_res[0][1],
                            'sid': info_res[0][2]
                        }
                        return student_data

        if formatted == 'json':
            return HttpResponse(json.dumps([]) , content_type="application/json")
        else:
            return {}

def GetLanguageId(language_name=None):
    language  = Languages.objects.get(name__exact=language_name)  # @UndefinedVariable
    return language.id

def GetLevelId(level_name=None):
    level = PlacementLevels.objects.get( Q(level__exact=level_name)&  # @UndefinedVariable
                                         Q(active__exact = 1)
                                         )  # @UndefinedVariable
    return level.id  