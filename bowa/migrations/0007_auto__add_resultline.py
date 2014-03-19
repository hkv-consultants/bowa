# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ResultLine'
        db.create_table('bowa_resultline', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('scenario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bowa.BowaScenario'])),
            ('sim', self.gf('django.db.models.fields.IntegerField')()),
            ('toetseenheid', self.gf('django.db.models.fields.IntegerField')()),
            ('functie', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('toetshoogte', self.gf('django.db.models.fields.FloatField')()),
            ('volume', self.gf('django.db.models.fields.FloatField')()),
            ('oppervlakte', self.gf('django.db.models.fields.FloatField')()),
            ('percentage', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('bowa', ['ResultLine'])


    def backwards(self, orm):
        
        # Deleting model 'ResultLine'
        db.delete_table('bowa_resultline')


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
        },
        'bowa.resultline': {
            'Meta': {'object_name': 'ResultLine'},
            'functie': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'oppervlakte': ('django.db.models.fields.FloatField', [], {}),
            'percentage': ('django.db.models.fields.FloatField', [], {}),
            'scenario': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bowa.BowaScenario']"}),
            'sim': ('django.db.models.fields.IntegerField', [], {}),
            'toetseenheid': ('django.db.models.fields.IntegerField', [], {}),
            'toetshoogte': ('django.db.models.fields.FloatField', [], {}),
            'volume': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['bowa']
