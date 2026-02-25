from django.urls import path
from .views import DashboardOverviewView, DashboardActivityView, DashboardAnalyticsView

urlpatterns = [
    path('overview/', DashboardOverviewView.as_view(), name='dashboard_overview'),
    path('activity/', DashboardActivityView.as_view(), name='dashboard_activity'),
    path('analytics/', DashboardAnalyticsView.as_view(), name='dashboard_analytics'),
]
