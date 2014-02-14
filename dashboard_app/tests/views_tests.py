"""Tests for the views of the dashboard_app."""
from django.test import TestCase

from django_libs.tests.mixins import ViewRequestFactoryTestMixin
from django_libs.tests.factories import UserFactory

from ..import views


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
