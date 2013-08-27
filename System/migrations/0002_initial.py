# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SchoolProfile'
        db.create_table(u'System_schoolprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('school_profile', self.gf('django.db.models.fields.related.OneToOneField')(related_name='school_profile', unique=True, to=orm['auth.User'])),
            ('Zip_code', self.gf('django.db.models.fields.CharField')(max_length=9, null=True)),
        ))
        db.send_create_signal(u'System', ['SchoolProfile'])

        # Adding model 'Classes'
        db.create_table(u'System_classes', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('School', self.gf('django.db.models.fields.related.ForeignKey')(related_name='school', null=True, to=orm['System.SchoolProfile'])),
            ('Class_Name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('Class_Description', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True)),
            ('Max_Occupancy', self.gf('django.db.models.fields.IntegerField')(max_length=300)),
            ('Teacher', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'System', ['Classes'])

        # Adding model 'User_profile'
        db.create_table(u'System_user_profile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_profile', self.gf('django.db.models.fields.related.OneToOneField')(related_name='user_profile', unique=True, to=orm['auth.User'])),
            ('School', self.gf('django.db.models.fields.related.ForeignKey')(related_name='School', null=True, to=orm['System.SchoolProfile'])),
            ('Class_chosen', self.gf('django.db.models.fields.related.OneToOneField')(related_name='class_chosen', unique=True, null=True, on_delete=models.SET_NULL, to=orm['System.Preference'])),
            ('Locked', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'System', ['User_profile'])

        # Adding model 'Preference'
        db.create_table(u'System_preference', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(related_name='student', null=True, on_delete=models.SET_NULL, to=orm['System.User_profile'])),
            ('rank', self.gf('django.db.models.fields.IntegerField')(max_length=1000)),
            ('Class', self.gf('django.db.models.fields.related.ForeignKey')(related_name='class', null=True, on_delete=models.SET_NULL, to=orm['System.Classes'])),
        ))
        db.send_create_signal(u'System', ['Preference'])


    def backwards(self, orm):
        # Deleting model 'SchoolProfile'
        db.delete_table(u'System_schoolprofile')

        # Deleting model 'Classes'
        db.delete_table(u'System_classes')

        # Deleting model 'User_profile'
        db.delete_table(u'System_user_profile')

        # Deleting model 'Preference'
        db.delete_table(u'System_preference')


    models = {
        u'System.classes': {
            'Class_Description': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'}),
            'Class_Name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'Max_Occupancy': ('django.db.models.fields.IntegerField', [], {'max_length': '300'}),
            'Meta': {'object_name': 'Classes'},
            'School': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'school'", 'null': 'True', 'to': u"orm['System.SchoolProfile']"}),
            'Teacher': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'System.preference': {
            'Class': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'class'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['System.Classes']"}),
            'Meta': {'object_name': 'Preference'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rank': ('django.db.models.fields.IntegerField', [], {'max_length': '1000'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'student'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['System.User_profile']"})
        },
        u'System.schoolprofile': {
            'Meta': {'object_name': 'SchoolProfile'},
            'Zip_code': ('django.db.models.fields.CharField', [], {'max_length': '9', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'school_profile': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'school_profile'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        u'System.user_profile': {
            'Class_chosen': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'class_chosen'", 'unique': 'True', 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['System.Preference']"}),
            'Locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'Meta': {'object_name': 'User_profile'},
            'School': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'School'", 'null': 'True', 'to': u"orm['System.SchoolProfile']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_profile': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'user_profile'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['System']