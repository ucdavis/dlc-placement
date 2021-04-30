'''
Created on Feb 4, 2016

@author: mauricio
'''
class LevelsRouter(object): 
    def db_for_read(self, model, **hints):
        "Point all operations on levels models to 'production'"
        if model._meta.app_label == 'levels':
            return 'production'
        return None

    def db_for_write(self, model, **hints):
        "Point all operations on levels models to 'production'"
        if model._meta.app_label == 'levels':
            return 'production'
        return None
    
    def allow_relation(self, obj1, obj2, **hints):
        "Allow relations if a model in the languages app is involved."
        if obj1._meta.app_label == 'levels' or \
           obj2._meta.app_label == 'levels':
                return True
        return None
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == 'production' or app_label == "levels":
            return None