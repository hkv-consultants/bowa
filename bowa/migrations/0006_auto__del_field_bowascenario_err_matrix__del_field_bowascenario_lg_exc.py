# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'BowaScenario.err_matrix'
        db.delete_column('bowa_bowascenario', 'err_matrix')

        # Deleting field 'BowaScenario.lg_excel'
        db.delete_column('bowa_bowascenario', 'lg_excel')

        # Adding field 'BowaScenario.fouten'
        db.add_column('bowa_bowascenario', 'fouten', self.gf('django.db.models.fields.FilePathField')(max_length=100, null=True, blank=True), keep_default=False)

        # Adding field 'BowaScenario.normen'
        db.add_column('bowa_bowascenario', 'normen', self.gf('django.db.models.fields.FilePathField')(max_length=100, null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'BowaScenario.err_matrix'
        db.add_column('bowa_bowascenario', 'err_matrix', self.gf('django.db.models.fields.FilePathField')(max_length=100, null=True, blank=True), keep_default=False)

        # Adding field 'BowaScenario.lg_excel'
        db.add_column('bowa_bowascenario', 'lg_excel', self.gf('django.db.models.fields.FilePathField')(max_length=100, null=True, blank=True), keep_default=False)

        # Deleting field 'BowaScenario.fouten'
        db.delete_column('bowa_bowascenario', 'fouten')

        # Deleting field 'BowaScenario.normen'
        db.delete_column('bowa_bowascenario', 'normen')


    models = {
        'bowa.bowascenario': {
            'Meta': {'object_name': 'BowaScenario'},
            'ah': ('django.db.models.fields.FilePathField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'ahdev': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'datetime_created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'expiration_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'fouten': ('django.db.models.fields.FilePathField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'ht10': ('django.db.models.fields.FilePathField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'ht100': ('django.db.models.fields.FilePathField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'ht25': ('django.db.models.fields.FilePathField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'ht50': ('django.db.models.fields.FilePathField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'htdev': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lg': ('django.db.models.fields.FilePathField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'normen': ('django.db.models.fields.FilePathField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'nsim': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pg': ('django.db.models.fields.FilePathField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'rho': ('django.db.models.fields.FloatField', [], {'default': '0.8'}),
            'scenario_type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'te': ('django.db.models.fields.FilePathField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['bowa']
