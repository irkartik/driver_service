"""
URL configuration for driver_service project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from drivers.views import DriverViewSet

# Create a router and register our viewsets with it
router = routers.DefaultRouter()
router.register(r'drivers', DriverViewSet, basename='driver')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/', include('drivers.urls')),
]

