"""Tests for the Widget Pool of the dashboard_app."""
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

from ..exceptions import WidgetAlreadyRegistered
from ..widget_pool import (
    DashboardWidgetPool,
    dashboard_widget_pool,
)

from .mixins import WidgetTestCaseMixin
from .test_widget_app.dashboard_widgets import DummyWidget


class FalseWidget(object):
    """
    This class will not be accepted as a widget.

    Because it does not inherit ``WidgetBase``.

    """
    pass


class DashboardWidgetPoolTestCase(WidgetTestCaseMixin, TestCase):
    """Tests for the ``WidgetPool`` class."""
    longMessage = True

    def test_instantiates_on_import(self):
        """
        Should instantiate WidgetPool when module is imported.

        """
        self.assertEqual(
            dashboard_widget_pool.__class__, DashboardWidgetPool, msg=(
                'When importing from `widget_pool`, an instance of'
                ' `WidgetPool` should be created'))

    def test_register_false_widget(self):
        """
        register_widget should raise exception if widget does not inherit

        ``DashboardWidgetBase``.

        """
        self.assertRaises(
            ImproperlyConfigured, dashboard_widget_pool.register_widget,
            FalseWidget)

    def test_register_widget(self):
        """register_widget should add the widget to ``self.widgets``."""
        self._unregister_widgets()
        dashboard_widget_pool.register_widget(DummyWidget)
        self.assertTrue('DummyWidget' in dashboard_widget_pool.widgets)

    def test_register_already_registered(self):
        """
        register_widget should raise exception if widget is already registered.

        """
        self._unregister_widgets()
        dashboard_widget_pool.register_widget(DummyWidget)
        self.assertRaises(
            WidgetAlreadyRegistered, dashboard_widget_pool.register_widget,
            DummyWidget)

    def test_unregister_widget(self):
        """
        unregister_widget should be remove the widget from ``self.widgets``.

        """
        self._unregister_widgets()
        dashboard_widget_pool.register_widget(DummyWidget)
        dashboard_widget_pool.unregister_widget(DummyWidget)
        self.assertEqual(dashboard_widget_pool.widgets, {})

    def test_1_discover_widgets(self):
        """
        discover_widgets Should find widgets in INSTALLED_APPS.

        When called again, it should not nothing.

        This test must be executed first before any other test messes around
        with the registered widgets.

        """
        dashboard_widget_pool.discover_widgets()
        self.assertTrue('DummyWidget' in dashboard_widget_pool.widgets)
        self.assertTrue('DummyWidget2' in dashboard_widget_pool.widgets)

        dashboard_widget_pool.discover_widgets()
        self.assertTrue('DummyWidget' in dashboard_widget_pool.widgets)
        self.assertTrue('DummyWidget2' in dashboard_widget_pool.widgets)

    def test_get_widgets(self):
        """get_widgets should discover widgets and return them."""
        widgets = dashboard_widget_pool.get_widgets()
        self.assertEqual(widgets, dashboard_widget_pool.widgets)

    def test_get_widgets_sorted(self):
        """get_widgets_sorted should return the widgets sorted by position."""
        self._unregister_widgets()
        dashboard_widget_pool.register_widget(DummyWidget, position=3)
        dashboard_widget_pool.register_widget(
            DummyWidget, widget_name='w2', position=2)
        dashboard_widget_pool.register_widget(
            DummyWidget, widget_name='w3', position=1)
        result = dashboard_widget_pool.get_widgets_sorted()
        self.assertEqual(result[0][2], 1, msg=(
            'Should return the widget with position 1 first'))
        self.assertEqual(result[2][2], 3, msg=(
            'Should return the widget with position 3 last'))

    def test_get_widget(self):
        """get_widget should return the given widget."""
        dashboard_widget_pool.discover_widgets()
        widget = dashboard_widget_pool.get_widget('DummyWidget')
        self.assertEqual(widget.get_name(), 'DummyWidget', msg=(
            'Should return the correct widget'))
