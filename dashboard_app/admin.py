"""Admin classes for the dashboard_app app."""
from django.contrib import admin

from . import models


class DashboardWidgetLastUpdateAdmin(admin.ModelAdmin):
    list_display = ['widget_name', 'last_update', ]
    search_fields = ['widget_name', ]


class DashboardWidgetSettingsAdmin(admin.ModelAdmin):
    list_display = ['widget_name', 'setting_name', 'value']
    search_fields = ['widget_name', 'setting_name', 'value', ]


admin.site.register(
    models.DashboardWidgetLastUpdate, DashboardWidgetLastUpdateAdmin)
admin.site.register(
    models.DashboardWidgetSettings, DashboardWidgetSettingsAdmin)
