from django.test import TestCase
from django.core.urlresolvers import reverse
from django.db.models import get_model
from django.conf import settings

from .models import create_fields, create_models, load_models


TEST_FIELDS = [
        {"id": "string", "title": "String", "type": "char"},
        {"id": "number", "title": "Number", "type": "int"},
        {"id": "date", "title": "Date", "type": "date"}
]


class SimpleTest(TestCase):

    def test_create_fields(self):
        fields = create_fields(TEST_FIELDS)
        self.assertIs(fields['string'].get_internal_type(), 'CharField')
        self.assertIs(fields['number'].get_internal_type(), 'IntegerField')
        self.assertIs(fields['date'].get_internal_type(), 'DateField')

    def test_create_model(self):
        name = "some_model"
        title = "Some model"
        model = create_models(name, title, create_fields(TEST_FIELDS))
        self.assertEqual(model.__name__, name)
        self.assertEqual(model._meta.verbose_name, title)
        self.assertEqual(model._meta.verbose_name_plural, title)
        self.assertEqual(len(model._meta.fields), 4)

    def test_main_page(self):
        response = self.client.get(reverse('main-page'))
        self.assertEqual(response.status_code, 200)

    def test_show_model(self):
        load_models(settings.LOAD_MODELS_FROM)
        response = self.client.get(reverse('show-model'),
                {'model_name': ' rooms '},
                HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response['content-type'], 'application/json')
        self.assertContains(response, 'table_headers')
        self.assertContains(response, 'objects')
        self.assertContains(response, 'table_fields')

        #add new object
        response = self.client.get(reverse('add-object'),
                {'model_name': ' rooms ',
                 'fields[]': ["department", "spots", "last_repair", "windows"],
                 'values[]': ["new_department", "2", "2013-01-31", "5"]},
                HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        model = get_model('core', 'rooms')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(model.objects.count(), 1)
        self.assertEqual(model.objects.get(id=1).spots, 2)

        #edit field
        response = self.client.get(reverse('edit-field'),
                {'model_name': ' rooms ',
                 'object_id': 1,
                 'field_name': 'windows',
                 'new_value': '10'},
                HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(model.objects.get(id=1).windows, 10)
