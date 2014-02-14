# flake8: noqa
# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DashboardWidgetLastUpdate'
        db.create_table(u'dashboard_app_dashboardwidgetlastupdate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('widget_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'dashboard_app', ['DashboardWidgetLastUpdate'])

        # Adding model 'DashboardWidgetSettings'
        db.create_table(u'dashboard_app_dashboardwidgetsettings', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('widget_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('setting_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=4000)),
        ))
        db.send_create_signal(u'dashboard_app', ['DashboardWidgetSettings'])

        # Adding unique constraint on 'DashboardWidgetSettings', fields ['widget_name', 'setting_name']
        db.create_unique(u'dashboard_app_dashboardwidgetsettings', ['widget_name', 'setting_name'])


    def backwards(self, orm):
        # Removing unique constraint on 'DashboardWidgetSettings', fields ['widget_name', 'setting_name']
        db.delete_unique(u'dashboard_app_dashboardwidgetsettings', ['widget_name', 'setting_name'])

        # Deleting model 'DashboardWidgetLastUpdate'
        db.delete_table(u'dashboard_app_dashboardwidgetlastupdate')

        # Deleting model 'DashboardWidgetSettings'
        db.delete_table(u'dashboard_app_dashboardwidgetsettings')


    models = {
        u'dashboard_app.dashboardwidgetlastupdate': {
            'Meta': {'object_name': 'DashboardWidgetLastUpdate'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'widget_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'dashboard_app.dashboardwidgetsettings': {
            'Meta': {'unique_together': "(('widget_name', 'setting_name'),)", 'object_name': 'DashboardWidgetSettings'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'setting_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '4000'}),
            'widget_name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['dashboard_app']
