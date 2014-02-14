"""Tests for the widget base class of the dashboard_app."""
import time

from django.test import TestCase

from .. import models
from ..widget_base import DashboardWidgetBase
from .test_widget_app.dashboard_widgets import DummyWidget


class DashboardWidgetBaseTestCase(TestCase):
    """Tests for the ``DashboardWidgetBase`` base class."""
    longMessage = True

    def test_get_context_data(self):
        """get_context_data should return the widget name by default."""
        base = DashboardWidgetBase()
        result = base.get_context_data()
        self.assertEqual(result['widget_name'], base.get_name())

    def test_get_name(self):
        """
        get_name should return the class name when called on a child class.

        """
        widget = DummyWidget()
        result = widget.get_name()
        self.assertEqual(result, 'DummyWidget')

    def test_get_setting(self):
        """get_setting should get the setting from the database."""
        widget = DummyWidget()
        setting = widget.get_setting('IS_ENABLED')
        self.assertEqual(setting, None, msg=(
            'Should return None if the setting does not exist in the db'))
        widget.save_setting('IS_ENABLED', '1')
        setting = widget.get_setting('IS_ENABLED')
        self.assertEqual(setting.setting_name, 'IS_ENABLED', msg=(
            'Should return the correct setting from the database when called'))

    def test_get_title(self):
        """get_title should return the title of the widget."""
        widget = DummyWidget()
        result = widget.get_title()
        self.assertEqual(result, widget.get_name(), msg=(
            'The default implementation should just return the class name'))

    def test_update_widget_data_not_implemented(self):
        """update_widget_data should throw exception if not implemented."""
        base = DashboardWidgetBase()
        self.assertRaises(NotImplementedError, base.update_widget_data)

    def test_save_setting(self):
        """save_setting should save the value to the database."""
        widget = DummyWidget()
        setting = widget.save_setting('IS_ENABLED', '1')
        self.assertTrue(setting.pk, msg=(
            'Should create a new DB entry when saving the setting for the'
            ' first time'))
        self.assertEqual(setting.value, '1', msg=(
            'Should set the correct value on the new setting object'))

        setting2 = widget.save_setting('IS_ENABLED', '0')
        self.assertEqual(setting, setting2, msg=(
            'Should not create a new object if that setting already exists'
            ' in the database'))
        self.assertEqual(setting2.value, '0', msg=(
            'Should update the setting value on save'))

    def test_set_last_update(self):
        """
        set_last_update should save the last update in the settings table.

        """
        widget = DummyWidget()
        widget.set_last_update()
        last_update = models.DashboardWidgetLastUpdate.objects.get(
            widget_name=widget.get_name())
        self.assertTrue(last_update.last_update)

    def test_should_update(self):
        widget = DummyWidget()
        result = widget.should_update()
        self.assertFalse(result, msg=(
            'Right after creation it should not update because the last update'
            ' date will be set to now and this test will happen faster than'
            ' one second later'))
        time.sleep(1)
        result = widget.should_update()
        self.assertTrue(result, msg=(
            'After one second it should return true because the last update'
            ' was longer ago than the update interval of the DummyWidget'))
