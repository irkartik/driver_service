# Driver Service API v1 - Endpoint Reference

All API endpoints now use the `/api/v1/` prefix for versioning.

## Base URL

```
http://127.0.0.1:8000/api/v1/
```

## Complete Endpoint List

### CRUD Operations

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/drivers/` | List all drivers (paginated) |
| POST | `/api/v1/drivers/` | Create a new driver |
| GET | `/api/v1/drivers/{id}/` | Get specific driver details |
| PUT | `/api/v1/drivers/{id}/` | Full update of a driver |
| PATCH | `/api/v1/drivers/{id}/` | Partial update of a driver |
| DELETE | `/api/v1/drivers/{id}/` | Delete a driver |

### Filtering & Search

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/drivers/active/` | Get all active drivers |
| GET | `/api/v1/drivers/inactive/` | Get all inactive drivers |
| GET | `/api/v1/drivers/by_vehicle_type/?vehicle_type=Sedan` | Get drivers by vehicle type |
| GET | `/api/v1/drivers/?search=query` | Search drivers by name/phone/plate |
| GET | `/api/v1/drivers/?vehicle_type=Sedan` | Filter by vehicle type |
| GET | `/api/v1/drivers/?is_active=true` | Filter by active status |

### Status Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/drivers/{id}/toggle_status/` | Toggle driver active/inactive status |
| POST | `/api/v1/drivers/{id}/activate/` | Activate a driver |
| POST | `/api/v1/drivers/{id}/deactivate/` | Deactivate a driver |

### Statistics & Details

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/drivers/stats/` | Get driver statistics |
| GET | `/api/v1/drivers/{id}/details/` | Get detailed driver information |
| GET | `/api/v1/drivers/{id}/status/` | Get driver status information |

## Quick Examples

### Get All Drivers
```bash
curl http://127.0.0.1:8000/api/v1/drivers/
```

### Get Specific Driver
```bash
curl http://127.0.0.1:8000/api/v1/drivers/1/
```

### Create Driver
```bash
curl -X POST http://127.0.0.1:8000/api/v1/drivers/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "phone": "9876543210",
    "vehicle_type": "Sedan",
    "vehicle_plate": "KA01AB1234",
    "is_active": true
  }'
```

### Update Driver Status
```bash
curl -X POST http://127.0.0.1:8000/api/v1/drivers/1/toggle_status/
```

### Get Statistics
```bash
curl http://127.0.0.1:8000/api/v1/drivers/stats/
```

### Get Driver Status
```bash
curl http://127.0.0.1:8000/api/v1/drivers/1/status/
```

### Search Drivers
```bash
curl "http://127.0.0.1:8000/api/v1/drivers/?search=Driver1"
```

### Filter Active Drivers
```bash
curl "http://127.0.0.1:8000/api/v1/drivers/?is_active=true"
```

### Filter by Vehicle Type
```bash
curl "http://127.0.0.1:8000/api/v1/drivers/?vehicle_type=Sedan"
```

## Browser Access

Open in your browser for interactive API:
- **API Root**: http://127.0.0.1:8000/api/v1/
- **Drivers List**: http://127.0.0.1:8000/api/v1/drivers/
- **Statistics**: http://127.0.0.1:8000/api/v1/drivers/stats/
- **Active Drivers**: http://127.0.0.1:8000/api/v1/drivers/active/

## Python Examples

```python
import requests

BASE_URL = "http://127.0.0.1:8000/api/v1"

# Get all drivers
response = requests.get(f"{BASE_URL}/drivers/")
print(response.json())

# Get specific driver
driver = requests.get(f"{BASE_URL}/drivers/1/")
print(driver.json())

# Create new driver
new_driver = {
    "name": "Jane Smith",
    "phone": "9999888877",
    "vehicle_type": "SUV",
    "vehicle_plate": "KA99ZZ9999",
    "is_active": True
}
response = requests.post(f"{BASE_URL}/drivers/", json=new_driver)
print(response.json())

# Toggle status
toggle = requests.post(f"{BASE_URL}/drivers/1/toggle_status/")
print(toggle.json())

# Get statistics
stats = requests.get(f"{BASE_URL}/drivers/stats/")
print(stats.json())

# Get driver status
status = requests.get(f"{BASE_URL}/drivers/1/status/")
print(status.json())

# Search drivers
search = requests.get(f"{BASE_URL}/drivers/", params={"search": "Driver1"})
print(search.json())

# Filter active drivers
active = requests.get(f"{BASE_URL}/drivers/", params={"is_active": "true"})
print(active.json())
```

## Response Examples

### GET /api/v1/drivers/1/
```json
{
  "driver_id": 1,
  "name": "Driver1",
  "phone": "9743818976",
  "vehicle_type": "Bike",
  "vehicle_plate": "KA98DX4733",
  "is_active": true,
  "created_at": "2025-10-19T19:20:21.766780+05:30",
  "updated_at": "2025-10-19T19:26:19.821882+05:30"
}
```

### GET /api/v1/drivers/stats/
```json
{
  "total_drivers": 70,
  "active_drivers": 50,
  "inactive_drivers": 20,
  "vehicle_type_distribution": {
    "Sedan": 16,
    "Hatchback": 15,
    "SUV": 15,
    "Bike": 14,
    "Auto": 10
  },
  "active_vehicle_type_distribution": {
    "Hatchback": 12,
    "Sedan": 12,
    "SUV": 11,
    "Bike": 9,
    "Auto": 6
  }
}
```

### GET /api/v1/drivers/{id}/status/
```json
{
  "driver_id": 1,
  "name": "Driver1",
  "is_active": true,
  "vehicle_type": "Bike",
  "vehicle_plate": "KA98DX4733",
  "last_updated": "2025-10-19T13:56:19.821882Z"
}
```

### GET /api/v1/drivers/ (Paginated)
```json
{
  "count": 70,
  "next": "http://127.0.0.1:8000/api/v1/drivers/?page=2",
  "previous": null,
  "results": [
    {
      "driver_id": 70,
      "name": "Driver70",
      "phone": "9073604213",
      "vehicle_type": "Bike",
      "vehicle_plate": "KA50ZP8276",
      "is_active": true,
      "status": "Active"
    },
    ...
  ]
}
```

## Pagination

All list endpoints support pagination:
- Default page size: 10 items
- Access pages: `?page=2`, `?page=3`, etc.
- Results include `count`, `next`, and `previous` links

## Filtering Combinations

You can combine multiple filters:

```bash
# Active Sedan drivers
curl "http://127.0.0.1:8000/api/v1/drivers/?is_active=true&vehicle_type=Sedan"

# Search in active drivers
curl "http://127.0.0.1:8000/api/v1/drivers/?is_active=true&search=Driver1"

# Sort by name
curl "http://127.0.0.1:8000/api/v1/drivers/?ordering=name"

# Sort by creation date (descending)
curl "http://127.0.0.1:8000/api/v1/drivers/?ordering=-created_at"
```

## Status Codes

- **200 OK**: Successful GET/PUT/PATCH
- **201 Created**: Successful POST
- **204 No Content**: Successful DELETE
- **400 Bad Request**: Invalid input
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server error

## Error Response Example

```json
{
  "phone": [
    "Phone number must be exactly 10 digits"
  ]
}
```

---

**Note**: All endpoints now use the `/api/v1/` prefix for API versioning.

