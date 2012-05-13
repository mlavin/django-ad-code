# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Section.priority'
        db.add_column('adcode_section', 'priority',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting field 'Section.priority'
        db.delete_column('adcode_section', 'priority')

    models = {
        'adcode.placement': {
            'Meta': {'object_name': 'Placement'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'remote_id': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '200', 'blank': 'True'}),
            'sections': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'placements'", 'blank': 'True', 'to': "orm['adcode.Section']"}),
            'size': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'placements'", 'to': "orm['adcode.Size']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        'adcode.section': {
            'Meta': {'object_name': 'Section'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'pattern': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'priority': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        'adcode.size': {
            'Meta': {'object_name': 'Size'},
            'height': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'width': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        }
    }

    complete_apps = ['adcode']