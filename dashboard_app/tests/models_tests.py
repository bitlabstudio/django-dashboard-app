"""Tests for the models of the ``django-metrics-dashboard`` app."""
from django.test import TestCase

from .. import models
from .factories import DashboardWidgetSettingsFactory


class DashboardWidgetLastUpdateTestCase(TestCase):
    """Tests for the ``DashboardWidgetLastUpdate`` model class."""
    longMessage = True

    def test_model(self):
        instance = models.DashboardWidgetLastUpdate()
        instance.save()
        self.assertTrue(instance.pk)


class DashboardWidgetSettingsTestCase(TestCase):
    """Tests for the ``DashboardWidgetSettings`` model class."""
    longMessage = True

    def test_model(self):
        instance = DashboardWidgetSettingsFactory()
        self.assertTrue(instance.pk)
