"""Views for the dashboard_app app."""
from django.views.generic import TemplateView, View

from . import view_mixins
from .widget_pool import dashboard_widget_pool


class DashboardNeedsUpdateView(view_mixins.JSONResponseMixin, View):
    """
    Returns a JSON list of widget names that need re-rendering.

    """
    def get(self, request, *args, **kwargs):
        widgets = dashboard_widget_pool.get_widgets_that_need_update()
        result = []
        for widget in widgets:
            result.append(widget.get_name())
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
        widgets = dashboard_widget_pool.get_widgets()
        ctx.update({
            'widgets': widgets,
        })
        return ctx
