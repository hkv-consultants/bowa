# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'BowaScenario.scenario_types'
        db.delete_column('bowa_bowascenario', 'scenario_types')

        # Adding field 'BowaScenario.scenario_type'
        db.add_column('bowa_bowascenario', 'scenario_type', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Changing field 'BowaScenario.rho'
        db.alter_column('bowa_bowascenario', 'rho', self.gf('django.db.models.fields.FloatField')())


    def backwards(self, orm):
        
        # Adding field 'BowaScenario.scenario_types'
        db.add_column('bowa_bowascenario', 'scenario_types', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Deleting field 'BowaScenario.scenario_type'
        db.delete_column('bowa_bowascenario', 'scenario_type')

        # Changing field 'BowaScenario.rho'
        db.alter_column('bowa_bowascenario', 'rho', self.gf('django.db.models.fields.FloatField')(null=True))


    models = {
        'bowa.bowascenario': {
            'Meta': {'object_name': 'BowaScenario'},
            'ah': ('django.db.models.fields.FilePathField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'ahdev': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'datetime_created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'err_matrix': ('django.db.models.fields.FilePathField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'expiration_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'ht10': ('django.db.models.fields.FilePathField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'ht100': ('django.db.models.fields.FilePathField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'ht25': ('django.db.models.fields.FilePathField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'ht50': ('django.db.models.fields.FilePathField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'htdev': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lg': ('django.db.models.fields.FilePathField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'lg_excel': ('django.db.models.fields.FilePathField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'nsim': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pg': ('django.db.models.fields.FilePathField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'rho': ('django.db.models.fields.FloatField', [], {'default': '0.8'}),
            'scenario_type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'te': ('django.db.models.fields.FilePathField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['bowa']
