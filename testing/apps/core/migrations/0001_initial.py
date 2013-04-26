# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'users'
        db.create_table('core_users', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            (u'paycheck', self.gf('django.db.models.fields.IntegerField')()),
            (u'date_joined', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('core', ['users'])

        # Adding model 'rooms'
        db.create_table('core_rooms', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'department', self.gf('django.db.models.fields.CharField')(max_length=255)),
            (u'spots', self.gf('django.db.models.fields.IntegerField')()),
            (u'last_repair', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('core', ['rooms'])


    def backwards(self, orm):
        # Deleting model 'users'
        db.delete_table('core_users')

        # Deleting model 'rooms'
        db.delete_table('core_rooms')


    models = {
        'core.rooms': {
            'Meta': {'object_name': 'rooms'},
            u'department': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'last_repair': ('django.db.models.fields.DateField', [], {}),
            u'spots': ('django.db.models.fields.IntegerField', [], {})
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