# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'ApiKey.api_key'
        db.alter_column(u'cfd_apikey', 'api_key', self.gf('django.db.models.fields.CharField')(max_length=56))

    def backwards(self, orm):

        # Changing field 'ApiKey.api_key'
        db.alter_column(u'cfd_apikey', 'api_key', self.gf('django.db.models.fields.CharField')(max_length=38))

    models = {
        u'cfd.apikey': {
            'Meta': {'object_name': 'ApiKey'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'api_key': ('django.db.models.fields.CharField', [], {'max_length': '56'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cfd.Server']"})
        },
        u'cfd.fact': {
            'Meta': {'object_name': 'Fact'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cfd.Server']"}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        u'cfd.server': {
            'Meta': {'object_name': 'Server'},
            'hostname': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['cfd']