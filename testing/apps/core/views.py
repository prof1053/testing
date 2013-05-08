from django.shortcuts import render
from django.db.models import get_models, get_app, get_model

from annoying.decorators import ajax_request


def main_page(request):
    models = get_models(get_app(__name__.split('.')[0]))
    models_list=[]
    for m in models:
        models_list.append(m._meta.object_name)
    return render(request, 'main_page.html', {'models': models_list})


@ajax_request
def show_model(request):
    model_name = request.GET.get('model_name', None)
    string = __name__.split('.')[0]+model_name
    model = get_model(*string.split(' '))

    fields = model._meta.fields
    table_headers = [field.verbose_name for field in fields]

    table_fields = []
    for field in fields:
        table_fields.append([field.name, field.get_internal_type()])

    objects = {}
    data = []
    for object in model.objects.all():
        for field in object._meta.fields:
            if field.get_internal_type() == 'DateField':
                setattr(object, field.name, getattr(object,field.name).strftime("%Y-%m-%d"))
            data.append([field.name, getattr(object,field.name), field.get_internal_type()])
        objects[object.id] = data
        data = []
    return {'table_headers': table_headers, 'table_fields': table_fields, 'objects': objects, 'model': model_name}


@ajax_request
def edit_field(request):
    model_name = request.GET.get('model_name', None)
    object_id = request.GET.get('object_id', None)
    field_name = request.GET.get('field_name', None)
    new_value = request.GET.get('new_value', None)

    string = __name__.split('.')[0]+model_name
    model = get_model(*string.split(' '))
    object = model.objects.get(id=object_id)

    setattr(object, field_name, new_value)
    object.save()

    return {'success': 'success'}


@ajax_request
def add_object(request):
    model_name = request.GET.get('model_name', None)
    fields = request.GET.getlist('fields[]', None)
    values = request.GET.getlist('values[]', None)

    dictionary = dict(zip(fields, values))

    string = __name__.split('.')[0]+model_name
    model = get_model(*string.split(' '))

    new_object = model()
    for field, (key, value) in enumerate(dictionary.items()):
        setattr(new_object, key, value)
    new_object.save()

    object = {}
    data = []
    for field in new_object._meta.fields:
        data.append([field.name, getattr(new_object, field.name), field.get_internal_type()])
    object[new_object.id] = data

    return {'success': 'success', 'object': object, 'model': model_name}
