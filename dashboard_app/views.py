"""Views for the dashboard_app app."""
from django.conf import settings
from django.http import Http404, HttpResponse
from django.template.defaultfilters import date
from django.views.generic import TemplateView, View

import requests

from . import view_mixins
from .dashboard_widgets import RemoteWidget
from .widget_pool import dashboard_widget_pool


class DashboardLastUpdateView(view_mixins.JSONResponseMixin, View):
    """Returns a JSON dict of widgets and their last update time."""
    def get(self, request, *args, **kwargs):
        widgets = dashboard_widget_pool.get_widgets_that_need_update()
        result = {}
        for widget in widgets:
            result[widget.get_name()] = date(
                widget.get_last_update().last_update, "c")
        return self.render_to_response(result)


class DashboardView(view_mixins.PermissionRequiredViewMixin, TemplateView):
    """
    Main view of the app. Displays the metrics dashboard.

    Widgets on the dashboard get loaded individually via AJAX calls against
    the ``DashboardAPIWidgetView``.

    """
    template_name = 'dashboard_app/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super(DashboardView, self).get_context_data(**kwargs)
        widgets = dashboard_widget_pool.get_widgets_sorted()
        ctx.update({
            'widgets': widgets,
        })
        return ctx


class DashboardRenderWidgetView(view_mixins.PermissionRequiredViewMixin,
                                view_mixins.RenderWidgetMixin,
                                TemplateView):
    """AJAX view that renders any given widget by name."""
    def dispatch(self, request, *args, **kwargs):
        self.widget = dashboard_widget_pool.get_widget(
            request.GET.get('name'))
        if isinstance(self.widget, RemoteWidget):
            url = self.widget.url
            payload = {
                'token': self.widget.token,
                'name': self.widget.remote_widget_name,
            }
            r = requests.get(url, params=payload)
            return HttpResponse(r.text)
        return super(DashboardRenderWidgetView, self).dispatch(
            request, *args, **kwargs)


class DashboardGetRemoteWidgetView(view_mixins.RenderWidgetMixin,
                                   TemplateView):
    """
    Returns a widget as requested by a remote server.

    """
    def dispatch(self, request, *args, **kwargs):
        self.widget_name = request.GET.get('name')
        self.widget = dashboard_widget_pool.get_widget(self.widget_name)
        self.token = request.GET.get('token')
        self.access = getattr(settings, 'DASHBOARD_REMOTE_ACCESS', {})
        if not self.widget_name in self.access:
            raise Http404
        if not self.token in self.access[self.widget_name]:
            raise Http404
        return super(DashboardGetRemoteWidgetView, self).dispatch(
            request, *args, **kwargs)
