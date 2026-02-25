from django.contrib import admin
from django.urls import path, include
from core.views import LandingView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', LandingView.as_view(), name='landing'),
    path('admin/', admin.site.urls),
    
    # Authentication
    path('api/auth/', include('users.urls')),

    # Apps
    path('api/core/', include('core.urls')),
    path('api/integrations/', include('integrations.urls')),
    path('api/custom/', include('dashboard.urls')),
    path('api/dashboard/', include('dashboard.dashboard_urls')),
    path('dashboard/', include('dashboard.ui_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
