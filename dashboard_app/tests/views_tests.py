"""Tests for the views of the dashboard_app."""
import time

from django.test import TestCase

from django_libs.tests.mixins import ViewRequestFactoryTestMixin
from django_libs.tests.factories import UserFactory


from . import mixins
from .. import views
from ..widget_pool import dashboard_widget_pool


class DashboardLastUpdateViewTestCase(ViewRequestFactoryTestMixin,
                                      mixins.WidgetTestCaseMixin,
                                      TestCase):
    """Tests for the ``DashboardLastUpdateView`` view class."""
    longMessage = True
    view_class = views.DashboardLastUpdateView

    def setUp(self):
        super(DashboardLastUpdateViewTestCase, self).setUp()
        self.superuser = UserFactory(is_superuser=True)
        self.normal_user = UserFactory()

        # This ensures that we have one last update in the database
        dashboard_widget_pool.get_widgets_that_need_update()
        time.sleep(1)

    def test_view(self):
        resp = self.get(ajax=True)
        self.assertTrue('DummyWidget' in resp.content, msg=(
            'Should return a list all widgets that need an update'))


class DashboardViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``DashboardView`` view class."""
    longMessage = True
    view_class = views.DashboardView

    def setUp(self):
        super(DashboardViewTestCase, self).setUp()
        self.superuser = UserFactory(is_superuser=True)
        self.normal_user = UserFactory()

    def test_security(self):
        self.should_redirect_to_login_when_anonymous()

        resp = self.get(user=self.normal_user)
        self.assertEqual(resp.status_code, 302, msg=(
            "Should redirect to login if the user doesn't have the correct"
            " permissions"))

        with self.settings(DASHBOARD_REQUIRE_LOGIN=False):
            resp = self.get()
            self.assertEqual(resp.status_code, 200, msg=(
                'When REQUIRE_LOGIN is False, anyone should be able to see the'
                ' view'))

    def test_view(self):
        resp = self.get(user=self.superuser)
        self.assertEqual(resp.status_code, 200, msg=(
            'User with correct permissions should be able to see the view'))
