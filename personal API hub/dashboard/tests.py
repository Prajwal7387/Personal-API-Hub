from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class DashboardRouteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_landing_page_redirect_anonymous(self):
        """Landing page should load for anonymous users."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_landing_page_redirect_authenticated(self):
        """Landing page should redirect to overview for authenticated users."""
        self.client.login(username='testuser', password='password123')
        response = self.client.get('/')
        self.assertRedirects(response, reverse('ui_overview'))

    def test_dashboard_routes_require_login(self):
        """All dashboard UI routes should redirect to login if not authenticated."""
        routes = ['ui_overview', 'ui_integrations', 'ui_analytics', 'ui_builder', 'ui_settings']
        for route in routes:
            response = self.client.get(reverse(route))
            self.assertEqual(response.status_code, 302)

    def test_dashboard_routes_load_authenticated(self):
        """All dashboard UI routes should load for authenticated users."""
        self.client.login(username='testuser', password='password123')
        routes = ['ui_overview', 'ui_integrations', 'ui_analytics', 'ui_builder', 'ui_settings']
        for route in routes:
            response = self.client.get(reverse(route))
            self.assertEqual(response.status_code, 200, f"Route {route} failed to load.")
