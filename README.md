# Driver Service - Ride-Hailing Application

A Django REST API service for managing drivers in a ride-hailing application system.

## Features

- **Complete CRUD Operations**: Create, Read, Update, and Delete drivers
- **Driver Status Management**: Activate/deactivate drivers
- **Advanced Filtering**: Filter by status, vehicle type, search by name, phone, or vehicle plate
- **Statistics API**: Get driver statistics and distributions
- **CSV Data Import**: Load driver data from CSV files
- **Admin Interface**: Django admin panel for easy management
- **REST API**: Fully RESTful API with proper HTTP methods
- **API Documentation**: Browsable API with DRF

## Technology Stack

- **Backend Framework**: Django 4.2.7
- **API Framework**: Django REST Framework 3.14.0
- **Database**: SQLite (default), PostgreSQL ready
- **Python Version**: 3.8+

## Project Structure

```
driver_service/
├── driver_service/          # Project configuration
│   ├── __init__.py
│   ├── settings.py         # Django settings
│   ├── urls.py             # Main URL configuration
│   ├── asgi.py
│   └── wsgi.py
├── drivers/                 # Drivers app
│   ├── management/
│   │   └── commands/
│   │       └── load_drivers.py  # CSV import command
│   ├── migrations/         # Database migrations
│   ├── __init__.py
│   ├── admin.py           # Admin interface
│   ├── apps.py
│   ├── models.py          # Driver model
│   ├── serializers.py     # DRF serializers
│   ├── tests.py           # Unit tests
│   ├── urls.py            # App URLs
│   └── views.py           # API views
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Installation

### 1. Clone the repository

```bash
cd /Users/raju.jha/Downloads/ScalableServices/driver_service
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a superuser (for admin access)

```bash
python manage.py createsuperuser
```

### 6. Load seed data from CSV

```bash
# Load from the default location
python manage.py load_drivers ../AssignmentStatement/rhfd_seed\ dataset/rhfd_drivers.csv

# Or with clearing existing data
python manage.py load_drivers ../AssignmentStatement/rhfd_seed\ dataset/rhfd_drivers.csv --clear
```

### 7. Run the development server

```bash
python manage.py runserver
```

The server will start at `http://127.0.0.1:8000/`

## API Endpoints

### Base URL: `http://127.0.0.1:8000/api/`

### Driver Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/drivers/` | List all drivers (paginated) |
| POST | `/api/drivers/` | Create a new driver |
| GET | `/api/drivers/{id}/` | Get a specific driver |
| PUT | `/api/drivers/{id}/` | Update a driver (full update) |
| PATCH | `/api/drivers/{id}/` | Partially update a driver |
| DELETE | `/api/drivers/{id}/` | Delete a driver |
| GET | `/api/drivers/active/` | Get all active drivers |
| GET | `/api/drivers/inactive/` | Get all inactive drivers |
| GET | `/api/drivers/by_vehicle_type/?vehicle_type=Sedan` | Get drivers by vehicle type |
| POST | `/api/drivers/{id}/toggle_status/` | Toggle driver active status |
| POST | `/api/drivers/{id}/activate/` | Activate a driver |
| POST | `/api/drivers/{id}/deactivate/` | Deactivate a driver |
| GET | `/api/drivers/stats/` | Get driver statistics |
| GET | `/api/drivers/{id}/details/` | Get detailed driver information |

### Request/Response Examples

#### Create a Driver

**Request:**
```bash
POST /api/drivers/
Content-Type: application/json

{
    "name": "John Doe",
    "phone": "9876543210",
    "vehicle_type": "Sedan",
    "vehicle_plate": "KA01AB1234",
    "is_active": true
}
```

**Response:**
```json
{
    "driver_id": 1,
    "name": "John Doe",
    "phone": "9876543210",
    "vehicle_type": "Sedan",
    "vehicle_plate": "KA01AB1234",
    "is_active": true,
    "status": "Active",
    "created_at": "2025-10-19T10:30:00Z",
    "updated_at": "2025-10-19T10:30:00Z"
}
```

#### Get All Drivers

**Request:**
```bash
GET /api/drivers/
```

**Response:**
```json
{
    "count": 70,
    "next": "http://127.0.0.1:8000/api/drivers/?page=2",
    "previous": null,
    "results": [
        {
            "driver_id": 1,
            "name": "Driver1",
            "phone": "9743818976",
            "vehicle_type": "Bike",
            "vehicle_plate": "KA98DX4733",
            "is_active": false,
            "status": "Inactive"
        },
        ...
    ]
}
```

#### Get Driver Statistics

**Request:**
```bash
GET /api/drivers/stats/
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

#### Filter and Search

```bash
# Get active drivers only
GET /api/drivers/?is_active=true

# Search by name
GET /api/drivers/?search=Driver1

# Filter by vehicle type
GET /api/drivers/?vehicle_type=Sedan

# Combine filters
GET /api/drivers/?is_active=true&vehicle_type=SUV&search=Driver

# Order by name
GET /api/drivers/?ordering=name

# Order by creation date (descending)
GET /api/drivers/?ordering=-created_at
```

## Data Model

### Driver

| Field | Type | Description |
|-------|------|-------------|
| driver_id | Integer (PK) | Unique driver identifier |
| name | String | Driver's full name |
| phone | String | 10-digit phone number (unique) |
| vehicle_type | String | Type of vehicle (Bike, Auto, Hatchback, Sedan, SUV) |
| vehicle_plate | String | Vehicle registration plate (unique) |
| is_active | Boolean | Whether driver is active |
| created_at | DateTime | Record creation timestamp |
| updated_at | DateTime | Record last update timestamp |

## Admin Interface

Access the Django admin panel at `http://127.0.0.1:8000/admin/`

Features:
- List all drivers with filters
- Search by name, phone, or vehicle plate
- Bulk activate/deactivate drivers
- Edit driver information
- View creation and update timestamps

## Testing

Run the test suite:

```bash
# Run all tests
python manage.py test

# Run tests with coverage
pytest --cov=drivers

# Run specific test class
python manage.py test drivers.tests.DriverModelTests

# Run specific test method
python manage.py test drivers.tests.DriverAPITests.test_create_driver
```

## Management Commands

### Load Drivers from CSV

```bash
python manage.py load_drivers <path_to_csv_file>

# Options:
# --clear: Clear existing drivers before loading
python manage.py load_drivers rhfd_drivers.csv --clear
```

## Development

### Code Style

The project follows PEP 8 guidelines. Use these tools for code quality:

```bash
# Format code with black
black .

# Sort imports
isort .

# Check code style
flake8
```

### Making Changes

1. Create a new branch
2. Make your changes
3. Run tests to ensure everything works
4. Format code with black and isort
5. Submit your changes

## API Response Formats

All API responses follow REST conventions:

- **200 OK**: Successful GET, PUT, PATCH
- **201 Created**: Successful POST
- **204 No Content**: Successful DELETE
- **400 Bad Request**: Invalid input data
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server error

Error responses include detailed messages:

```json
{
    "field_name": [
        "Error message"
    ]
}
```

## Configuration

### Database Configuration

To use PostgreSQL instead of SQLite, update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'driver_service_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Environment Variables

For production, use environment variables for sensitive data:

```bash
export SECRET_KEY='your-secret-key'
export DEBUG=False
export DATABASE_URL='postgresql://user:pass@localhost/dbname'
```

## Deployment

For production deployment:

1. Set `DEBUG = False` in settings.py
2. Configure a production database (PostgreSQL)
3. Set up a proper SECRET_KEY
4. Configure ALLOWED_HOSTS
5. Use a production web server (gunicorn, uwsgi)
6. Set up HTTPS
7. Configure static files serving

## Support

For issues or questions, please refer to the assignment documentation or contact the development team.

## License

This project is created for educational purposes as part of the Scalable Services assignment.


