from django.db import models


def create_model(name, fields=None, module='', options=None):
    class Meta:
        pass

    if options is not None:
        for key, value in options.iteritems():
            setattr(Meta, key, value)

    attrs = {'__module__': module, 'Meta': Meta}

    if fields:
        attrs.update(fields)

    return type(name, (models.Model,), attrs)
