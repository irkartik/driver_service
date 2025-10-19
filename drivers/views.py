from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Count, Q
from .models import Driver
from .serializers import (
    DriverSerializer,
    DriverListSerializer,
    DriverCreateUpdateSerializer,
    DriverStatusSerializer
)


class DriverViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Driver CRUD operations and custom actions.
    
    list: Get all drivers
    retrieve: Get a specific driver by ID
    create: Create a new driver
    update: Update a driver (full update)
    partial_update: Partially update a driver
    destroy: Delete a driver
    
    Custom actions:
    - active: Get all active drivers
    - inactive: Get all inactive drivers
    - by_vehicle_type: Get drivers by vehicle type
    - toggle_status: Toggle driver active status
    - stats: Get driver statistics
    """
    
    queryset = Driver.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active', 'vehicle_type']
    search_fields = ['name', 'phone', 'vehicle_plate']
    ordering_fields = ['driver_id', 'name', 'created_at', 'vehicle_type']
    ordering = ['-driver_id']
    
    def get_serializer_class(self):
        """
        Return appropriate serializer class based on action.
        """
        if self.action == 'list':
            return DriverListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return DriverCreateUpdateSerializer
        elif self.action == 'toggle_status':
            return DriverStatusSerializer
        return DriverSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Create a new driver.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Return full driver details
        driver = Driver.objects.get(pk=serializer.instance.pk)
        response_serializer = DriverSerializer(driver)
        
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )
    
    def update(self, request, *args, **kwargs):
        """
        Update a driver (full update).
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # Return full driver details
        driver = Driver.objects.get(pk=instance.pk)
        response_serializer = DriverSerializer(driver)
        
        return Response(response_serializer.data)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Get all active drivers.
        GET /api/drivers/active/
        """
        active_drivers = self.queryset.filter(is_active=True)
        
        # Apply search and filters
        active_drivers = self.filter_queryset(active_drivers)
        
        page = self.paginate_queryset(active_drivers)
        if page is not None:
            serializer = DriverListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = DriverListSerializer(active_drivers, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def inactive(self, request):
        """
        Get all inactive drivers.
        GET /api/drivers/inactive/
        """
        inactive_drivers = self.queryset.filter(is_active=False)
        
        # Apply search and filters
        inactive_drivers = self.filter_queryset(inactive_drivers)
        
        page = self.paginate_queryset(inactive_drivers)
        if page is not None:
            serializer = DriverListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = DriverListSerializer(inactive_drivers, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_vehicle_type(self, request):
        """
        Get drivers by vehicle type.
        GET /api/drivers/by_vehicle_type/?vehicle_type=Sedan
        """
        vehicle_type = request.query_params.get('vehicle_type', None)
        
        if not vehicle_type:
            return Response(
                {"error": "vehicle_type parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        drivers = self.queryset.filter(vehicle_type__iexact=vehicle_type)
        
        # Apply search and filters
        drivers = self.filter_queryset(drivers)
        
        page = self.paginate_queryset(drivers)
        if page is not None:
            serializer = DriverListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = DriverListSerializer(drivers, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post', 'patch'])
    def toggle_status(self, request, pk=None):
        """
        Toggle driver active status.
        POST /api/drivers/{id}/toggle_status/
        """
        driver = self.get_object()
        driver.is_active = not driver.is_active
        driver.save()
        
        serializer = DriverSerializer(driver)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post', 'patch'])
    def activate(self, request, pk=None):
        """
        Activate a driver.
        POST /api/drivers/{id}/activate/
        """
        driver = self.get_object()
        driver.is_active = True
        driver.save()
        
        serializer = DriverSerializer(driver)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post', 'patch'])
    def deactivate(self, request, pk=None):
        """
        Deactivate a driver.
        POST /api/drivers/{id}/deactivate/
        """
        driver = self.get_object()
        driver.is_active = False
        driver.save()
        
        serializer = DriverSerializer(driver)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Get driver statistics.
        GET /api/drivers/stats/
        """
        total_drivers = self.queryset.count()
        active_drivers = self.queryset.filter(is_active=True).count()
        inactive_drivers = self.queryset.filter(is_active=False).count()
        
        # Count by vehicle type
        vehicle_type_stats = self.queryset.values('vehicle_type').annotate(
            count=Count('vehicle_type')
        ).order_by('-count')
        
        # Count active drivers by vehicle type
        active_vehicle_stats = self.queryset.filter(is_active=True).values('vehicle_type').annotate(
            count=Count('vehicle_type')
        ).order_by('-count')
        
        stats = {
            'total_drivers': total_drivers,
            'active_drivers': active_drivers,
            'inactive_drivers': inactive_drivers,
            'vehicle_type_distribution': {
                item['vehicle_type']: item['count'] 
                for item in vehicle_type_stats
            },
            'active_vehicle_type_distribution': {
                item['vehicle_type']: item['count'] 
                for item in active_vehicle_stats
            }
        }
        
        return Response(stats)
    
    @action(detail=True, methods=['get'])
    def details(self, request, pk=None):
        """
        Get detailed information about a driver.
        GET /api/drivers/{id}/details/
        """
        driver = self.get_object()
        serializer = DriverSerializer(driver)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], url_path='status')
    def driver_status(self, request, pk=None):
        """
        Get the status of a specific driver.
        GET /api/v1/drivers/{id}/status
        """
        driver = self.get_object()
        
        status_data = {
            'driver_id': driver.driver_id,
            'name': driver.name,
            'is_active': driver.is_active,
            'vehicle_type': driver.vehicle_type,
            'vehicle_plate': driver.vehicle_plate,
            'last_updated': driver.updated_at
        }
        
        return Response(status_data)

