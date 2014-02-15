"""Useful mixins for views."""
from django import http
from django.utils import simplejson as json
from django.utils.decorators import method_decorator

from .decorators import permission_required


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


class JSONResponseMixin(object):
    """Mixin to convert the response content into a JSON response."""
    def render_to_response(self, context):
        "Returns a JSON response containing 'context' as payload"
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return http.HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        return json.dumps(context)
