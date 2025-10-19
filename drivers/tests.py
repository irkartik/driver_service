from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Driver


class DriverModelTests(TestCase):
    """
    Test cases for Driver model.
    """
    
    def setUp(self):
        self.driver = Driver.objects.create(
            name='Test Driver',
            phone='9876543210',
            vehicle_type='Sedan',
            vehicle_plate='KA01AB1234',
            is_active=True
        )
    
    def test_driver_creation(self):
        """Test that a driver can be created successfully"""
        self.assertEqual(self.driver.name, 'Test Driver')
        self.assertEqual(self.driver.phone, '9876543210')
        self.assertEqual(self.driver.vehicle_type, 'Sedan')
        self.assertEqual(self.driver.vehicle_plate, 'KA01AB1234')
        self.assertTrue(self.driver.is_active)
    
    def test_driver_string_representation(self):
        """Test the string representation of driver"""
        expected = f"{self.driver.name} ({self.driver.vehicle_type} - {self.driver.vehicle_plate})"
        self.assertEqual(str(self.driver), expected)
    
    def test_driver_status_property(self):
        """Test the status property"""
        self.assertEqual(self.driver.status, "Active")
        self.driver.is_active = False
        self.assertEqual(self.driver.status, "Inactive")


class DriverAPITests(APITestCase):
    """
    Test cases for Driver API endpoints.
    """
    
    def setUp(self):
        self.driver1 = Driver.objects.create(
            name='Driver One',
            phone='9876543210',
            vehicle_type='Sedan',
            vehicle_plate='KA01AB1234',
            is_active=True
        )
        
        self.driver2 = Driver.objects.create(
            name='Driver Two',
            phone='9876543211',
            vehicle_type='SUV',
            vehicle_plate='KA01AB1235',
            is_active=False
        )
    
    def test_list_drivers(self):
        """Test listing all drivers"""
        url = reverse('driver-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_retrieve_driver(self):
        """Test retrieving a specific driver"""
        url = reverse('driver-detail', kwargs={'pk': self.driver1.driver_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Driver One')
    
    def test_create_driver(self):
        """Test creating a new driver"""
        url = reverse('driver-list')
        data = {
            'name': 'New Driver',
            'phone': '9876543212',
            'vehicle_type': 'Bike',
            'vehicle_plate': 'KA01AB1236',
            'is_active': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Driver.objects.count(), 3)
    
    def test_update_driver(self):
        """Test updating a driver"""
        url = reverse('driver-detail', kwargs={'pk': self.driver1.driver_id})
        data = {
            'name': 'Updated Driver',
            'phone': '9876543210',
            'vehicle_type': 'SUV',
            'vehicle_plate': 'KA01AB1234',
            'is_active': True
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.driver1.refresh_from_db()
        self.assertEqual(self.driver1.name, 'Updated Driver')
        self.assertEqual(self.driver1.vehicle_type, 'SUV')
    
    def test_delete_driver(self):
        """Test deleting a driver"""
        url = reverse('driver-detail', kwargs={'pk': self.driver1.driver_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Driver.objects.count(), 1)
    
    def test_get_active_drivers(self):
        """Test getting active drivers"""
        url = reverse('driver-active')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_get_inactive_drivers(self):
        """Test getting inactive drivers"""
        url = reverse('driver-inactive')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_get_drivers_by_vehicle_type(self):
        """Test getting drivers by vehicle type"""
        url = reverse('driver-by-vehicle-type')
        response = self.client.get(url, {'vehicle_type': 'Sedan'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_toggle_driver_status(self):
        """Test toggling driver status"""
        url = reverse('driver-toggle-status', kwargs={'pk': self.driver1.driver_id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.driver1.refresh_from_db()
        self.assertFalse(self.driver1.is_active)
    
    def test_get_driver_stats(self):
        """Test getting driver statistics"""
        url = reverse('driver-stats')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_drivers'], 2)
        self.assertEqual(response.data['active_drivers'], 1)
        self.assertEqual(response.data['inactive_drivers'], 1)

