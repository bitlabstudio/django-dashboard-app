"""Factories for the dashboard_app."""
import factory

from .. import models


class DashboardWidgetSettingsFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.DashboardWidgetSettings

    widget_name = 'my_widget'
    setting_name = 'my_setting'
    value = '1'
