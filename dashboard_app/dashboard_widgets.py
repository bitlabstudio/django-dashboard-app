"""Built-in widgets for the dashboard_app."""
from django.utils.timezone import now

from dashboard_app.widget_base import DashboardWidgetBase


class DummyWidget(DashboardWidgetBase):
    """Use this widget to test your installation."""
    template_name = 'dashboard_app/widgets/dummy_widget.html'

    def get_context_data(self, **kwargs):
        ctx = super(DummyWidget, self).get_context_data(**kwargs)
        ctx.update({'value': now(), })
        return ctx
