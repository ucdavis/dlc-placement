'''
Created on Feb 4, 2016

@author: mauricio
'''
class LanguageRouter(object): 
    def db_for_read(self, model, **hints):
        "Point all operations on languages models to 'production'"
        if model._meta.app_label == 'languages':
            return 'production'
        return None

    def db_for_write(self, model, **hints):
        "Point all operations on languages models to 'production'"
        if model._meta.app_label == 'languages':
            return 'production'
        return None
    
    def allow_relation(self, obj1, obj2, **hints):
        "Allow relations if a model in the languages app is involved."
        if obj1._meta.app_label == 'languages' or \
           obj2._meta.app_label == 'languages':
                return True
        return None
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == 'production' or app_label == "languages":
            return None