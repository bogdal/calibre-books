
class DbRouter(object):

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'calibre':
            return 'calibre'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'calibre':
            return None
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'calibre' or \
           obj2._meta.app_label == 'calibre':
           return True
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):
        if db == 'calibre':
            return model._meta.app_label == 'calibre'
        elif model and model._meta.app_label == 'calibre':
            return False
        return None
