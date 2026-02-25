from django.urls import path
from .views import CustomAPICreateView, DynamicCustomAPIView

urlpatterns = [
    path('create/', CustomAPICreateView.as_view(), name='custom_api_create'),
    path('<str:endpoint_name>/', DynamicCustomAPIView.as_view(), name='custom_api_execute'),
]
