# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Section'
        db.create_table('adcode_section', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100)),
            ('pattern', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('adcode', ['Section'])

        # Adding model 'Size'
        db.create_table('adcode_size', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('width', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('height', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('adcode', ['Size'])

        # Adding model 'Placement'
        db.create_table('adcode_placement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100)),
            ('remote_id', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('size', self.gf('django.db.models.fields.related.ForeignKey')(related_name='placements', to=orm['adcode.Size'])),
        ))
        db.send_create_signal('adcode', ['Placement'])

        # Adding M2M table for field sections on 'Placement'
        db.create_table('adcode_placement_sections', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('placement', models.ForeignKey(orm['adcode.placement'], null=False)),
            ('section', models.ForeignKey(orm['adcode.section'], null=False))
        ))
        db.create_unique('adcode_placement_sections', ['placement_id', 'section_id'])

    def backwards(self, orm):
        # Deleting model 'Section'
        db.delete_table('adcode_section')

        # Deleting model 'Size'
        db.delete_table('adcode_size')

        # Deleting model 'Placement'
        db.delete_table('adcode_placement')

        # Removing M2M table for field sections on 'Placement'
        db.delete_table('adcode_placement_sections')

    models = {
        'adcode.placement': {
            'Meta': {'object_name': 'Placement'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'remote_id': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'sections': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'placements'", 'symmetrical': 'False', 'to': "orm['adcode.Section']"}),
            'size': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'placements'", 'to': "orm['adcode.Size']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        'adcode.section': {
            'Meta': {'object_name': 'Section'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'pattern': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
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