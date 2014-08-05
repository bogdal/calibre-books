
class DbRouter(object):

    def db_for_read(self, model, **hints):

        if model._meta.app_label == 'calibre':
            return 'calibre'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'calibre':
            return None
        return 'default'
