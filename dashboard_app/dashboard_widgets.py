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


class RemoteWidget(DashboardWidgetBase):
    """Widget that renders a widget from another dashboard_app instance."""
    def __init__(self, url, token, remote_widget_name, **kwargs):
        """
        Initiates the widget.

        :param url: The URL of the remote dashboard api
          (i.e. http://example.com/dashboard/api/widget/)
        :param token: The API token you have been given by the admin of the
          remote server in order to obtain this widget.
        :remote_widget_name: The widget name as registered on the remote
          server.

        """
        self.url = url
        self.token = token
        self.remote_widget_name = remote_widget_name
        super(RemoteWidget, self).__init__(**kwargs)
