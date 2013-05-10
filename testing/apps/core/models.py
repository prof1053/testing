import json
import os.path

from django.db.models import CharField, IntegerField, DateField, Model
from django.contrib import admin
from django.conf import settings
from django.contrib.admin.sites import AlreadyRegistered


ALLOWED_FIELDS = {
    'char': CharField,
    'int': IntegerField,
    'date': DateField
}


def load_models(data_file):
    """
     Function that open json file where models are descripted,
     send received data to functions that creates fields and models,
     and register obtained models in the admin.
    """
    if os.path.exists(data_file):
        models_text = json.load(open(data_file, 'r'))
        for name, description in models_text.items():
            fields = create_fields(description['fields'])
            model = create_models(name, description['title'], fields)
            try:
                admin.site.register(model)
            except AlreadyRegistered:
                pass

def create_fields(text_fields):
    """
     Function that create model fields from text description
     and add max_lenght attr to CharField
    """
    fields = {}
    for field in text_fields:
        if field['type'] in ALLOWED_FIELDS.keys():
            if field['type'] == 'char':
                model_field = ALLOWED_FIELDS[field['type']](field['title'],
                                                            max_length=255)
            else:
                model_field = ALLOWED_FIELDS[field['type']](field['title'])
            fields[field['id']] = model_field
    return fields


def create_models(name, title, fields):
    """
     Function that create models from text description
    """
    Meta = type('Meta', (), {'verbose_name': title,
                             'verbose_name_plural': title,
                             'app_label': __name__.split(".")[0]})
    attrs = {'__module__': __name__, 'Meta': Meta}
    attrs.update(fields)
    return type(str(name), (Model,), attrs)


load_models(settings.LOAD_MODELS_FROM)
