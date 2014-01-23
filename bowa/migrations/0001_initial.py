# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'BowaScenario'
        db.create_table('bowa_bowascenario', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('ht10', self.gf('django.db.models.fields.FilePathField')(max_length=100, null=True, blank=True)),
            ('ht25', self.gf('django.db.models.fields.FilePathField')(max_length=100, null=True, blank=True)),
            ('ht50', self.gf('django.db.models.fields.FilePathField')(max_length=100, null=True, blank=True)),
            ('ht100', self.gf('django.db.models.fields.FilePathField')(max_length=100, null=True, blank=True)),
            ('pg', self.gf('django.db.models.fields.FilePathField')(max_length=100, null=True, blank=True)),
            ('lg', self.gf('django.db.models.fields.FilePathField')(max_length=100, null=True, blank=True)),
            ('ah', self.gf('django.db.models.fields.FilePathField')(max_length=100, null=True, blank=True)),
            ('te', self.gf('django.db.models.fields.FilePathField')(max_length=100, null=True, blank=True)),
            ('deviation_ah', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('deviation_h', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('num_simulations', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('scenario_types', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(db_index=True, max_length=50, null=True, blank=True)),
            ('datetime_created', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('expiration_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('bowa', ['BowaScenario'])


    def backwards(self, orm):
        
        # Deleting model 'BowaScenario'
        db.delete_table('bowa_bowascenario')


    models = {
        'bowa.bowascenario': {
            'Meta': {'object_name': 'BowaScenario'},
            'ah': ('django.db.models.fields.FilePathField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'datetime_created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'deviation_ah': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'deviation_h': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'expiration_date': ('django.db.models.fields.DateTimeField', [], {}),
            'ht10': ('django.db.models.fields.FilePathField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'ht100': ('django.db.models.fields.FilePathField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'ht25': ('django.db.models.fields.FilePathField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'ht50': ('django.db.models.fields.FilePathField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lg': ('django.db.models.fields.FilePathField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'num_simulations': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pg': ('django.db.models.fields.FilePathField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'scenario_types': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'te': ('django.db.models.fields.FilePathField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['bowa']
