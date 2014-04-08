"""Base DashboardWidget of the dashboard_app."""
from django.utils.timezone import now

from . import models


class DashboardWidgetBase(object):
    """All DashboardWidgets must inherit this base class."""
    update_interval = 1
    template_name = 'dashboard_app/partials/widget.html'

    def __init__(self, **kwargs):
        """
        Allows to initialise the widget with special options.

        :param widget_name: By setting the name, you override the get_name
          method and always return that name instead. This allows you to
          register the same widget class several times with different names.

        """
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def get_context_data(self):
        """
        Should return a dictionary of template context variables that are
        needed to render this widget.

        """
        return {'is_rendered': True, }

    def get_last_update(self):
        """Gets or creates the last update object for this widget."""
        instance, created = \
            models.DashboardWidgetLastUpdate.objects.get_or_create(
                widget_name=self.get_name())
        return instance

    def get_name(self):
        """
        Returns the class name of this widget.

        Be careful when overriding this. If ``self.widget_name`` is set, you
        should always return that in order to allow to register this widget
        class several times with different names.

        """
        if hasattr(self, 'widget_name'):
            return self.widget_name
        return self.__class__.__name__

    def get_setting(self, setting_name, default=None):
        """
        Returns the setting for this widget from the database.

        :setting_name: The name of the setting.
        :default: Optional default value if the setting cannot be found.

        """
        try:
            setting = models.DashboardWidgetSettings.objects.get(
                widget_name=self.get_name(),
                setting_name=setting_name)
        except models.DashboardWidgetSettings.DoesNotExist:
            setting = default
        return setting

    def get_title(self):
        """
        Returns the title of this widget.

        This should be shown on the dashboard.

        """
        return self.get_name()

    def save_setting(self, setting_name, value):
        """Saves the setting value into the database."""
        setting = self.get_setting(setting_name)
        if setting is None:
            setting = models.DashboardWidgetSettings.objects.create(
                widget_name=self.get_name(),
                setting_name=setting_name,
                value=value)
        setting.value = value
        setting.save()
        return setting

    def set_last_update(self):
        """Sets the last update time to ``now()``."""
        last_update = self.get_last_update()
        last_update.save()  # The model has auto_now_update=True

    def should_update(self):
        """
        Checks if an update is needed.

        Checks against ``self.update_interval`` and this widgets
        ``DashboardWidgetLastUpdate`` instance if an update is overdue.

        This should be called by
        ``DashboardWidgetPool.get_widgets_that_need_update()``, which in turn
        should be called by an admin command which should be scheduled every
        minute via crontab.

        """
        last_update = self.get_last_update()
        time_since = now() - last_update.last_update
        if time_since.seconds < self.update_interval:
            return False
        return True

    def update_widget_data(self):
        """
        Implement this in your widget in order to update the widget's data.

        This is the place where you would call some third party API, retrieve
        some data and save it into your widget's model.

        """
        raise NotImplementedError
