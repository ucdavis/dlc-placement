from django.shortcuts import render
from .forms import LanguageForm, StudentForm, LastNameForm
from languages_users.models import LanguagesUsersView
from languages.models import Languages



def SearchForm(request):
    if('user_id' in request.session):
            user_id= request.session['user_id']
# Get languages for user depending on assigned roles
            language_choices = [['','All Languages']]  
            if ('is_tester' in request.session) and ('is_admin' not in request.session):
                queryset_languages_user = LanguagesUsersView.objects.filter(user_id__exact=user_id).order_by('language_name')  # @UndefinedVariable                
                for data in queryset_languages_user:
                    language_choices.append([data.language_id,data.language_name])
            else:
                queryset_languages_user = Languages.objects.all().order_by('name')  # @UndefinedVariable 
                for data in queryset_languages_user:
                    language_choices.append([data.id,data.name]) 
# Form for language/period searching                             
            formLanguage =LanguageForm(request.GET or None,language_choices=language_choices)
# Form for last name searching       
            formLastName = LastNameForm(request.GET or None)
          
# Form for Student ID seaching     
            formStudent = StudentForm(request.GET or None)       
            
        
            context ={
                     'formLanguage' : formLanguage,
                     'formStudent' : formStudent,
                     'formLastName' : formLastName
                      }

            return render(request, 'home.html', context)
    else:
        return render(request, 'index.html') 
            
        
def index(request):
    return render(request, 'index.html')    