# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TrialProjectApplication'
        db.create_table(u'kguser_trialprojectapplication', (
            (u'projectapplication_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['applications.ProjectApplication'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'kguser', ['TrialProjectApplication'])


    def backwards(self, orm):
        # Deleting model 'TrialProjectApplication'
        db.delete_table(u'kguser_trialprojectapplication')


    models = {
        u'applications.application': {
            'Meta': {'object_name': 'Application'},
            '_class': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'complete_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['people.Person']", 'null': 'True', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'expires': ('django.db.models.fields.DateTimeField', [], {}),
            'header_message': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'secret_token': ('django.db.models.fields.CharField', [], {'default': "'b19123bf62457c748ecd696dbca4023103e66d9d'", 'unique': 'True', 'max_length': '64'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'submitted_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'applications.projectapplication': {
            'Meta': {'object_name': 'ProjectApplication', '_ormbases': [u'applications.Application']},
            'additional_req': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'application_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['applications.Application']", 'unique': 'True', 'primary_key': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'institute': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['institutes.Institute']", 'null': 'True', 'blank': 'True'}),
            'machine_categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['machines.MachineCategory']", 'null': 'True', 'blank': 'True'}),
            'make_leader': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'needs_account': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'pid': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.Project']", 'null': 'True', 'blank': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'institutes.institute': {
            'Meta': {'ordering': "['name']", 'object_name': 'Institute', 'db_table': "'institute'"},
            'delegates': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'delegate_for'", 'to': u"orm['people.Person']", 'through': u"orm['institutes.InstituteDelegate']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['people.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'saml_entityid': ('django.db.models.fields.CharField', [], {'max_length': '200', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'institutes.institutedelegate': {
            'Meta': {'object_name': 'InstituteDelegate', 'db_table': "'institutedelegate'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institute': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['institutes.Institute']"}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['people.Person']"}),
            'send_email': ('django.db.models.fields.BooleanField', [], {})
        },
        u'kguser.trialprojectapplication': {
            'Meta': {'object_name': 'TrialProjectApplication', '_ormbases': [u'applications.ProjectApplication']},
            u'projectapplication_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['applications.ProjectApplication']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'machines.machinecategory': {
            'Meta': {'object_name': 'MachineCategory', 'db_table': "'machine_category'"},
            'datastore': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'people.group': {
            'Meta': {'ordering': "['name']", 'object_name': 'Group'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'extra_data': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'foreign_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'groups'", 'symmetrical': 'False', 'to': u"orm['people.Person']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'people.person': {
            'Meta': {'ordering': "['full_name', 'short_name']", 'object_name': 'Person', 'db_table': "'person'"},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'approved_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user_approver'", 'null': 'True', 'to': u"orm['people.Person']"}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'date_approved': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_deleted': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'deleted_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user_deletor'", 'null': 'True', 'to': u"orm['people.Person']"}),
            'department': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'db_index': 'True'}),
            'expires': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institute': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['institutes.Institute']"}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_systemuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_usage': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'legacy_ldap_password': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'login_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'saml_id': ('django.db.models.fields.CharField', [], {'max_length': '200', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'supervisor': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'projects.project': {
            'Meta': {'ordering': "['pid']", 'object_name': 'Project', 'db_table': "'project'"},
            'additional_req': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'approved_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'project_approver'", 'null': 'True', 'to': u"orm['people.Person']"}),
            'date_approved': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_deleted': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'deleted_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'project_deletor'", 'null': 'True', 'to': u"orm['people.Person']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['people.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institute': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['institutes.Institute']"}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_usage': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'leaders': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'leads'", 'symmetrical': 'False', 'to': u"orm['people.Person']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'pid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 3, 27, 0, 0)'})
        }
    }

    complete_apps = ['kguser']
