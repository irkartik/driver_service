# Driver Service API Examples

This document provides practical examples for using the Driver Service API using `curl` and Python.

## Base URL

```
http://127.0.0.1:8000/api/
```

## Table of Contents

1. [CRUD Operations](#crud-operations)
2. [Filtering and Search](#filtering-and-search)
3. [Driver Status Management](#driver-status-management)
4. [Statistics](#statistics)
5. [Python Examples](#python-examples)

---

## CRUD Operations

### 1. Create a Driver

**cURL:**
```bash
curl -X POST http://127.0.0.1:8000/api/drivers/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Rajesh Kumar",
    "phone": "9876543210",
    "vehicle_type": "Sedan",
    "vehicle_plate": "KA01MN5678",
    "is_active": true
  }'
```

**Response:**
```json
{
  "driver_id": 71,
  "name": "Rajesh Kumar",
  "phone": "9876543210",
  "vehicle_type": "Sedan",
  "vehicle_plate": "KA01MN5678",
  "is_active": true,
  "status": "Active",
  "created_at": "2025-10-19T10:30:00.000000Z",
  "updated_at": "2025-10-19T10:30:00.000000Z"
}
```

### 2. Get All Drivers (with pagination)

**cURL:**
```bash
curl -X GET http://127.0.0.1:8000/api/drivers/
```

**Response:**
```json
{
  "count": 70,
  "next": "http://127.0.0.1:8000/api/drivers/?page=2",
  "previous": null,
  "results": [
    {
      "driver_id": 70,
      "name": "Driver70",
      "phone": "9122158681",
      "vehicle_type": "Bike",
      "vehicle_plate": "KA50ZP8276",
      "is_active": true,
      "status": "Active"
    },
    ...
  ]
}
```

### 3. Get a Specific Driver

**cURL:**
```bash
curl -X GET http://127.0.0.1:8000/api/drivers/1/
```

**Response:**
```json
{
  "driver_id": 1,
  "name": "Driver1",
  "phone": "9743818976",
  "vehicle_type": "Bike",
  "vehicle_plate": "KA98DX4733",
  "is_active": false,
  "status": "Inactive",
  "created_at": "2025-10-19T10:00:00.000000Z",
  "updated_at": "2025-10-19T10:00:00.000000Z"
}
```

### 4. Update a Driver (Full Update)

**cURL:**
```bash
curl -X PUT http://127.0.0.1:8000/api/drivers/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Driver1 Updated",
    "phone": "9743818976",
    "vehicle_type": "SUV",
    "vehicle_plate": "KA98DX4733",
    "is_active": true
  }'
```

### 5. Partial Update a Driver

**cURL:**
```bash
curl -X PATCH http://127.0.0.1:8000/api/drivers/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "vehicle_type": "Sedan",
    "is_active": true
  }'
```

### 6. Delete a Driver

**cURL:**
```bash
curl -X DELETE http://127.0.0.1:8000/api/drivers/1/
```

---

## Filtering and Search

### 1. Get Active Drivers

**cURL:**
```bash
curl -X GET "http://127.0.0.1:8000/api/drivers/active/"
```

### 2. Get Inactive Drivers

**cURL:**
```bash
curl -X GET "http://127.0.0.1:8000/api/drivers/inactive/"
```

### 3. Filter by Vehicle Type

**cURL:**
```bash
curl -X GET "http://127.0.0.1:8000/api/drivers/?vehicle_type=Sedan"
```

### 4. Search by Name, Phone, or Vehicle Plate

**cURL:**
```bash
# Search by name
curl -X GET "http://127.0.0.1:8000/api/drivers/?search=Driver1"

# Search by phone
curl -X GET "http://127.0.0.1:8000/api/drivers/?search=9876543210"

# Search by vehicle plate
curl -X GET "http://127.0.0.1:8000/api/drivers/?search=KA01"
```

### 5. Get Drivers by Specific Vehicle Type (Custom Endpoint)

**cURL:**
```bash
curl -X GET "http://127.0.0.1:8000/api/drivers/by_vehicle_type/?vehicle_type=SUV"
```

### 6. Combine Multiple Filters

**cURL:**
```bash
curl -X GET "http://127.0.0.1:8000/api/drivers/?is_active=true&vehicle_type=Sedan&search=Driver"
```

### 7. Ordering Results

**cURL:**
```bash
# Order by name (ascending)
curl -X GET "http://127.0.0.1:8000/api/drivers/?ordering=name"

# Order by name (descending)
curl -X GET "http://127.0.0.1:8000/api/drivers/?ordering=-name"

# Order by creation date (newest first)
curl -X GET "http://127.0.0.1:8000/api/drivers/?ordering=-created_at"
```

### 8. Pagination

**cURL:**
```bash
# Get specific page
curl -X GET "http://127.0.0.1:8000/api/drivers/?page=2"

# Change page size (if configured)
curl -X GET "http://127.0.0.1:8000/api/drivers/?page_size=20"
```

---

## Driver Status Management

### 1. Toggle Driver Status

**cURL:**
```bash
curl -X POST http://127.0.0.1:8000/api/drivers/1/toggle_status/
```

### 2. Activate a Driver

**cURL:**
```bash
curl -X POST http://127.0.0.1:8000/api/drivers/1/activate/
```

### 3. Deactivate a Driver

**cURL:**
```bash
curl -X POST http://127.0.0.1:8000/api/drivers/1/deactivate/
```

---

## Statistics

### Get Driver Statistics

**cURL:**
```bash
curl -X GET http://127.0.0.1:8000/api/drivers/stats/
```

**Response:**
```json
{
  "total_drivers": 70,
  "active_drivers": 45,
  "inactive_drivers": 25,
  "vehicle_type_distribution": {
    "Sedan": 15,
    "SUV": 18,
    "Hatchback": 15,
    "Bike": 12,
    "Auto": 10
  },
  "active_vehicle_type_distribution": {
    "SUV": 12,
    "Sedan": 10,
    "Hatchback": 10,
    "Bike": 8,
    "Auto": 5
  }
}
```

---

## Python Examples

### Using `requests` library

```python
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

# 1. Create a Driver
def create_driver():
    url = f"{BASE_URL}/drivers/"
    data = {
        "name": "Rajesh Kumar",
        "phone": "9876543210",
        "vehicle_type": "Sedan",
        "vehicle_plate": "KA01MN5678",
        "is_active": True
    }
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()

# 2. Get All Drivers
def get_all_drivers():
    url = f"{BASE_URL}/drivers/"
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Total Drivers: {data['count']}")
    return data

# 3. Get a Specific Driver
def get_driver(driver_id):
    url = f"{BASE_URL}/drivers/{driver_id}/"
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()

# 4. Update a Driver
def update_driver(driver_id):
    url = f"{BASE_URL}/drivers/{driver_id}/"
    data = {
        "name": "Updated Driver Name",
        "phone": "9876543210",
        "vehicle_type": "SUV",
        "vehicle_plate": "KA01MN5678",
        "is_active": True
    }
    response = requests.put(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()

# 5. Partial Update
def partial_update_driver(driver_id):
    url = f"{BASE_URL}/drivers/{driver_id}/"
    data = {
        "is_active": False
    }
    response = requests.patch(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()

# 6. Delete a Driver
def delete_driver(driver_id):
    url = f"{BASE_URL}/drivers/{driver_id}/"
    response = requests.delete(url)
    print(f"Status Code: {response.status_code}")
    return response.status_code == 204

# 7. Get Active Drivers
def get_active_drivers():
    url = f"{BASE_URL}/drivers/active/"
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Active Drivers: {len(data['results'])}")
    return data

# 8. Search Drivers
def search_drivers(query):
    url = f"{BASE_URL}/drivers/"
    params = {"search": query}
    response = requests.get(url, params=params)
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Found {data['count']} drivers")
    return data

# 9. Filter by Vehicle Type
def filter_by_vehicle_type(vehicle_type):
    url = f"{BASE_URL}/drivers/"
    params = {"vehicle_type": vehicle_type}
    response = requests.get(url, params=params)
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Found {data['count']} {vehicle_type} drivers")
    return data

# 10. Get Driver Statistics
def get_statistics():
    url = f"{BASE_URL}/drivers/stats/"
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()

# 11. Toggle Driver Status
def toggle_driver_status(driver_id):
    url = f"{BASE_URL}/drivers/{driver_id}/toggle_status/"
    response = requests.post(url)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()

# Example Usage
if __name__ == "__main__":
    # Create a new driver
    driver = create_driver()
    driver_id = driver['driver_id']
    
    # Get all drivers
    get_all_drivers()
    
    # Get specific driver
    get_driver(driver_id)
    
    # Search drivers
    search_drivers("Rajesh")
    
    # Filter by vehicle type
    filter_by_vehicle_type("Sedan")
    
    # Get statistics
    get_statistics()
    
    # Toggle status
    toggle_driver_status(driver_id)
    
    # Get active drivers
    get_active_drivers()
```

### Using `httpx` (Async)

```python
import httpx
import asyncio
import json

BASE_URL = "http://127.0.0.1:8000/api"

async def get_all_drivers_async():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/drivers/")
        data = response.json()
        print(f"Total Drivers: {data['count']}")
        return data

async def create_driver_async():
    async with httpx.AsyncClient() as client:
        data = {
            "name": "Async Driver",
            "phone": "9876543211",
            "vehicle_type": "Auto",
            "vehicle_plate": "KA01XY9999",
            "is_active": True
        }
        response = await client.post(f"{BASE_URL}/drivers/", json=data)
        print(f"Created: {json.dumps(response.json(), indent=2)}")
        return response.json()

# Run async functions
asyncio.run(get_all_drivers_async())
asyncio.run(create_driver_async())
```

---

## Error Handling

### Example: Invalid Phone Number

**Request:**
```bash
curl -X POST http://127.0.0.1:8000/api/drivers/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Driver",
    "phone": "123",
    "vehicle_type": "Sedan",
    "vehicle_plate": "KA01AB1234",
    "is_active": true
  }'
```

**Response (400 Bad Request):**
```json
{
  "phone": [
    "Phone number must be exactly 10 digits"
  ]
}
```

### Example: Duplicate Vehicle Plate

**Request:**
```bash
curl -X POST http://127.0.0.1:8000/api/drivers/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Driver",
    "phone": "9876543210",
    "vehicle_type": "Sedan",
    "vehicle_plate": "KA98DX4733",
    "is_active": true
  }'
```

**Response (400 Bad Request):**
```json
{
  "vehicle_plate": [
    "A driver with this vehicle plate already exists"
  ]
}
```

### Example: Driver Not Found

**Request:**
```bash
curl -X GET http://127.0.0.1:8000/api/drivers/999/
```

**Response (404 Not Found):**
```json
{
  "detail": "Not found."
}
```

---

## Tips

1. **Use the Browsable API**: Visit `http://127.0.0.1:8000/api/drivers/` in your browser to interact with the API visually.

2. **Pretty Print JSON**: Use `jq` for better JSON formatting:
   ```bash
   curl -X GET http://127.0.0.1:8000/api/drivers/1/ | jq
   ```

3. **Save Responses**: Save API responses to files:
   ```bash
   curl -X GET http://127.0.0.1:8000/api/drivers/ > drivers.json
   ```

4. **Testing**: Use tools like Postman, Insomnia, or HTTPie for easier API testing.

5. **Authentication**: If authentication is added later, include headers:
   ```bash
   curl -X GET http://127.0.0.1:8000/api/drivers/ \
     -H "Authorization: Bearer YOUR_TOKEN"
   ```


