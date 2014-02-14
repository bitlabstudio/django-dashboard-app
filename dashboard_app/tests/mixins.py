"""Mixins for the tests of the dashboard_app."""
from ..widget_pool import dashboard_widget_pool


class WidgetTestCaseMixin(object):
    """
    Mixin that makes sure to unregister widgets leftover from other tests.

    """
    def _unregister_widgets(self):
        # unregister all widgets that might be leftover from other tests
        dashboard_widget_pool.widgets = {}
        dashboard_widget_pool.discovered = False
