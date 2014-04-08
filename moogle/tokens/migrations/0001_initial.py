# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Provider'
        db.create_table('tokens_provider', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20, unique=True)),
            ('redirect_url', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('authorization_base_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('token_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('request_token_url', self.gf('django.db.models.fields.URLField')(blank=True, max_length=200)),
            ('oauth_version', self.gf('django.db.models.fields.CharField')(blank=True, max_length=5)),
            ('_scope', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('tokens', ['Provider'])

        # Adding model 'BearerToken'
        db.create_table('tokens_bearertoken', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('provider', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tokens.Provider'])),
            ('_access_token', self.gf('django.db.models.fields.TextField')()),
            ('updates_cursor', self.gf('django.db.models.fields.CharField')(blank=True, max_length=200)),
        ))
        db.send_create_signal('tokens', ['BearerToken'])

        # Adding unique constraint on 'BearerToken', fields ['user', 'provider']
        db.create_unique('tokens_bearertoken', ['user_id', 'provider_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'BearerToken', fields ['user', 'provider']
        db.delete_unique('tokens_bearertoken', ['user_id', 'provider_id'])

        # Deleting model 'Provider'
        db.delete_table('tokens_provider')

        # Deleting model 'BearerToken'
        db.delete_table('tokens_bearertoken')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'related_name': "'user_set'", 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'related_name': "'user_set'", 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'db_table': "'django_content_type'", 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'tokens.bearertoken': {
            'Meta': {'object_name': 'BearerToken', 'unique_together': "(('user', 'provider'),)"},
            '_access_token': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tokens.Provider']"}),
            'updates_cursor': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'tokens.provider': {
            'Meta': {'object_name': 'Provider'},
            '_scope': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'authorization_base_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'unique': 'True'}),
            'oauth_version': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '5'}),
            'redirect_url': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'request_token_url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200'}),
            'token_url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['tokens']