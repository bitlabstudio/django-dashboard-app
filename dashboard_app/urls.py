"""URLs for the dashboard_app app."""
from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'^$',
        views.DashboardView.as_view(),
        name='dashboard_app_dashboard'),
)
