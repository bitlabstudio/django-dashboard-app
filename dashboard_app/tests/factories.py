"""Factories for the dashboard_app."""
import factory

from .. import models


class DashboardWidgetLastUpdateFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.DashboardWidgetLastUpdate

    widget_name = factory.Sequence(lambda n: 'widget{0}'.format(n))


class DashboardWidgetSettingsFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.DashboardWidgetSettings

    widget_name = factory.Sequence(lambda n: 'widget{0}'.format(n))
    setting_name = 'setting_name'
    value = '1'
