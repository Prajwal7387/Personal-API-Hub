from django.urls import path
from .views import (
    OverviewUIView, IntegrationsUIView, AnalyticsUIView, 
    APIBuilderUIView, SettingsUIView
)

urlpatterns = [
    path('overview/', OverviewUIView.as_view(), name='ui_overview'),
    path('integrations/', IntegrationsUIView.as_view(), name='ui_integrations'),
    path('analytics/', AnalyticsUIView.as_view(), name='ui_analytics'),
    path('api-builder/', APIBuilderUIView.as_view(), name='ui_builder'),
    path('settings/', SettingsUIView.as_view(), name='ui_settings'),
]
