'''
Router for Scoresheet
Created on Feb, 2016

@author: mauricio
'''
class ScoresheetRouter(object): 
    def db_for_read(self, model, **hints):
        "Point all operations on scoresheet models to 'production'"
        if model._meta.app_label == 'scoresheet':
            return 'production'
        return None

    def db_for_write(self, model, **hints):
        "Point all operations on scoresheet models to 'production'"
        if model._meta.app_label == 'scoresheet':
            return 'production'
        return None
    
    def allow_relation(self, obj1, obj2, **hints):
        "Allow relations if a model in the languages app is involved."
        if obj1._meta.app_label == 'scoresheet' or \
           obj2._meta.app_label == 'scoresheet':
                return True
        return None
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == 'production' or app_label == "scoresheet":
            return None