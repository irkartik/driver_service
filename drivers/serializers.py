from rest_framework import serializers
from .models import Driver


class DriverSerializer(serializers.ModelSerializer):
    """
    Serializer for Driver model with all fields.
    """
    
    class Meta:
        model = Driver
        fields = [
            'driver_id',
            'name',
            'phone',
            'vehicle_type',
            'vehicle_plate',
            'is_active',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['driver_id', 'created_at', 'updated_at']
    
    def validate_phone(self, value):
        """
        Validate phone number format.
        """
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits")
        if len(value) != 10:
            raise serializers.ValidationError("Phone number must be exactly 10 digits")
        return value
    
    def validate_vehicle_plate(self, value):
        """
        Validate vehicle plate format.
        """
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("Vehicle plate cannot be empty")
        return value.strip().upper()


class DriverListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing drivers.
    """
    
    class Meta:
        model = Driver
        fields = [
            'driver_id',
            'name',
            'phone',
            'vehicle_type',
            'vehicle_plate',
            'is_active'
        ]


class DriverCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating drivers.
    """
    
    class Meta:
        model = Driver
        fields = [
            'name',
            'phone',
            'vehicle_type',
            'vehicle_plate',
            'is_active'
        ]
    
    def validate_phone(self, value):
        """
        Validate phone number format and uniqueness.
        """
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits")
        if len(value) != 10:
            raise serializers.ValidationError("Phone number must be exactly 10 digits")
        
        # Check uniqueness during update
        if self.instance:
            if Driver.objects.exclude(pk=self.instance.pk).filter(phone=value).exists():
                raise serializers.ValidationError("A driver with this phone number already exists")
        else:
            if Driver.objects.filter(phone=value).exists():
                raise serializers.ValidationError("A driver with this phone number already exists")
        
        return value
    
    def validate_vehicle_plate(self, value):
        """
        Validate vehicle plate format and uniqueness.
        """
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("Vehicle plate cannot be empty")
        
        value = value.strip().upper()
        
        # Check uniqueness during update
        if self.instance:
            if Driver.objects.exclude(pk=self.instance.pk).filter(vehicle_plate=value).exists():
                raise serializers.ValidationError("A driver with this vehicle plate already exists")
        else:
            if Driver.objects.filter(vehicle_plate=value).exists():
                raise serializers.ValidationError("A driver with this vehicle plate already exists")
        
        return value


class DriverStatusSerializer(serializers.ModelSerializer):
    """
    Serializer for updating driver status only.
    """
    
    class Meta:
        model = Driver
        fields = ['is_active']

