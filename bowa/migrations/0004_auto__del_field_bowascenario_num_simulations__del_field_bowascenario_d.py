# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'BowaScenario.num_simulations'
        db.delete_column('bowa_bowascenario', 'num_simulations')

        # Deleting field 'BowaScenario.deviation_ah'
        db.delete_column('bowa_bowascenario', 'deviation_ah')

        # Deleting field 'BowaScenario.deviation_h'
        db.delete_column('bowa_bowascenario', 'deviation_h')

        # Adding field 'BowaScenario.ahdev'
        db.add_column('bowa_bowascenario', 'ahdev', self.gf('django.db.models.fields.FloatField')(null=True, blank=True), keep_default=False)

        # Adding field 'BowaScenario.htdev'
        db.add_column('bowa_bowascenario', 'htdev', self.gf('django.db.models.fields.FloatField')(null=True, blank=True), keep_default=False)

        # Adding field 'BowaScenario.nsim'
        db.add_column('bowa_bowascenario', 'nsim', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'BowaScenario.rho'
        db.add_column('bowa_bowascenario', 'rho', self.gf('django.db.models.fields.FloatField')(null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'BowaScenario.num_simulations'
        db.add_column('bowa_bowascenario', 'num_simulations', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'BowaScenario.deviation_ah'
        db.add_column('bowa_bowascenario', 'deviation_ah', self.gf('django.db.models.fields.FloatField')(null=True, blank=True), keep_default=False)

        # Adding field 'BowaScenario.deviation_h'
        db.add_column('bowa_bowascenario', 'deviation_h', self.gf('django.db.models.fields.FloatField')(null=True, blank=True), keep_default=False)

        # Deleting field 'BowaScenario.ahdev'
        db.delete_column('bowa_bowascenario', 'ahdev')

        # Deleting field 'BowaScenario.htdev'
        db.delete_column('bowa_bowascenario', 'htdev')

        # Deleting field 'BowaScenario.nsim'
        db.delete_column('bowa_bowascenario', 'nsim')

        # Deleting field 'BowaScenario.rho'
        db.delete_column('bowa_bowascenario', 'rho')


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
            'rho': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'scenario_types': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'te': ('django.db.models.fields.FilePathField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['bowa']
