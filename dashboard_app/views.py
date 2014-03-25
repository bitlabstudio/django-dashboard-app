"""Views for the dashboard_app app."""
from django.views.generic import TemplateView, View
from django.template.defaultfilters import date

from . import view_mixins
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
                                TemplateView):
    """AJAX view that renders any given widget by name."""
    def dispatch(self, request, *args, **kwargs):
        self.widget = dashboard_widget_pool.get_widget(
            request.GET.get('name'))
        return super(DashboardRenderWidgetView, self).dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Adds ``is_rendered`` to the context and the widget's context data.

        ``is_rendered`` signals that the AJAX view has been called and that
        we are displaying the full widget now. When ``is_rendered`` is not
        found in the widget template it means that we are seeing the first
        page load and all widgets still have to get their real data from
        this AJAX view.

        """
        ctx = super(DashboardRenderWidgetView, self).get_context_data(**kwargs)
        ctx.update({
            'is_rendered': True,
            'widget': self.widget,
        })
        ctx.update(self.widget.get_context_data())
        return ctx

    def get_template_names(self):
        return [self.widget.template_name, ]
