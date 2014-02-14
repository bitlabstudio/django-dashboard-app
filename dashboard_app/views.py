"""Views for the dashboard_app app."""
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator

from dashboard_app.decorators import permission_required
# from dashboard_app.widget_pool import dashboard_widget_pool


class PermissionRequiredViewMixin(object):
    """
    Mixin to protect a view and require ``can_view_dashboard`` permission.

    Permission will only be required if the ``DASHBOARD_REQUIRE_LOGIN``
    setting is ``True``.

    """
    @method_decorator(
        permission_required('dashboard_app.can_view_dashboard'))
    def dispatch(self, request, *args, **kwargs):
        return super(PermissionRequiredViewMixin, self).dispatch(
            request, *args, **kwargs)


class DashboardView(PermissionRequiredViewMixin, TemplateView):
    """
    Main view of the app. Displays the metrics dashboard.

    Widgets on the dashboard get loaded individually via AJAX calls against
    the ``DashboardAPIWidgetView``.

    """
    template_name = 'dashboard_app/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super(DashboardView, self).get_context_data(**kwargs)
        widgets = [1, 2, 3, 4, 5, 6]  # dashboard_widget_pool.get_widgets()
        ctx.update({
            'widgets': widgets,
        })
        return ctx
