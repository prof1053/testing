# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'rooms.windows'
        db.add_column('core_rooms', u'windows',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'rooms.windows'
        db.delete_column('core_rooms', u'windows')


    models = {
        'core.rooms': {
            'Meta': {'object_name': 'rooms'},
            u'department': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'last_repair': ('django.db.models.fields.DateField', [], {}),
            u'spots': ('django.db.models.fields.IntegerField', [], {}),
            u'windows': ('django.db.models.fields.IntegerField', [], {})
        },
        'core.users': {
            'Meta': {'object_name': 'users'},
            u'date_joined': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'paycheck': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['core']