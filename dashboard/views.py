from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from .models import CustomAPI
from .serializers import CustomAPISerializer
from integrations.models import NormalizedData, ExternalAccount
from rest_framework.exceptions import NotFound

from core.utils.responses import success_response, error_response
from .services.analytics import AnalyticsService

from .services.custom_api import CustomAPIService
from core.analytics.processors.github_processor import GitHubProcessor
from core.analytics.visualizations.github_graphs import GitHubVisualizer

class CustomAPICreateView(generics.CreateAPIView):
    """
    POST /api/custom/create
    Allows users to create a new custom API configuration.
    """
    serializer_class = CustomAPISerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # We can also move this to CustomAPIService.create_custom_api if needed
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return success_response(serializer.data, "Custom API configuration created successfully.", status.HTTP_201_CREATED)
        return error_response("Invalid data provided.", status.HTTP_400_BAD_REQUEST, serializer.errors)

class DynamicCustomAPIView(APIView):
    """
    GET /api/custom/<endpoint_name>
    Loads the user's config and dynamically builds a response from normalized data via service layer.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, endpoint_name):
        try:
            # Shift complexity to the service layer
            response_data = CustomAPIService.execute_custom_api(request.user, endpoint_name)
            return success_response(response_data, "Custom API executed successfully.")
            
        except ValueError as e:
            return error_response(str(e), status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Handle NotFound or other exceptions
            if "not found" in str(e).lower():
                return error_response("Custom API endpoint not found.", status.HTTP_404_NOT_FOUND)
            return error_response("An error occurred during API execution.", status.HTTP_500_INTERNAL_SERVER_ERROR)

class DashboardOverviewView(APIView):
    """
    GET /api/dashboard/overview
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = AnalyticsService.get_overview_data(request.user)
        return success_response(data, "Overview data retrieved successfully.")

class DashboardActivityView(APIView):
    """
    GET /api/dashboard/activity
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = AnalyticsService.get_activity_data(request.user)
        return success_response(data, "Activity data retrieved successfully.")

class DashboardAnalyticsView(APIView):
    """
    GET /api/dashboard/analytics
    Processes normalized GitHub data and returns analytics with graph URLs.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # 1. Load normalized data
        try:
            github_data = NormalizedData.objects.get(user=request.user, source='github')
        except NormalizedData.DoesNotExist:
            return error_response("Normalized GitHub data not found. Please sync your GitHub account first.", status.HTTP_404_NOT_FOUND)

        # 2. Process data using pandas
        stats = GitHubProcessor.process(github_data.data)

        # 3. Generate graphs
        charts = GitHubVisualizer.generate_charts(request.user.id, stats)

        return success_response({
            "stats": stats,
            "charts": charts
        }, "Analytics generated successfully.")

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# --- UI Template Views ---

class OverviewUIView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/overview.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'overview'
        # In a real app, pull these from services
        context['integrations_count'] = NormalizedData.objects.filter(user=self.request.user).count()
        context['custom_apis_count'] = CustomAPI.objects.filter(user=self.request.user).count()
        context['recent_activities'] = [
            {'description': 'GitHub synchronization successful', 'timestamp': None},
            {'description': 'Custom API "user-profile" created', 'timestamp': None},
        ]
        return context

class IntegrationsUIView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/integrations.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'integrations'
        context['connected_providers'] = list(
            ExternalAccount.objects.filter(user=self.request.user)
            .values_list('provider', flat=True)
        )
        return context

class AnalyticsUIView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/analytics.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'analytics'
        return context

class APIBuilderUIView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/api_builder.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'builder'
        context['custom_apis'] = CustomAPI.objects.filter(user=self.request.user)
        return context

class SettingsUIView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/settings.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'settings'
        return context
