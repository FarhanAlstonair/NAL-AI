from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # API v1 Routes
    path('api/v1/auth/', include('nal_backend.apps.authentication.urls')),
    path('api/v1/users/', include('nal_backend.apps.users.urls')),
    path('api/v1/properties/', include('nal_backend.apps.properties.urls')),
    path('api/v1/documents/', include('nal_backend.apps.documents.urls')),
    path('api/v1/payments/', include('nal_backend.apps.payments.urls')),
    path('api/v1/bookings/', include('nal_backend.apps.bookings.urls')),
    path('api/v1/notifications/', include('nal_backend.apps.notifications.urls')),
    path('api/v1/analytics/', include('nal_backend.apps.analytics.urls')),
    path('api/v1/admin/', include('nal_backend.apps.admin_panel.urls')),
]