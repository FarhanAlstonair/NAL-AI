# NAL India Backend

A comprehensive property marketplace and verification platform built with Django and Django REST Framework.

## Features

- **Authentication & Authorization**: JWT-based auth with role-based access control
- **Property Management**: CRUD operations for properties with media support
- **Document Verification**: Automated OCR and ML-based document verification
- **Payment Integration**: Secure payment processing with webhook support
- **Booking System**: Property visit scheduling and management
- **Search & Discovery**: Advanced property search with location-based filtering
- **Admin Panel**: Comprehensive admin interface for platform management

## Tech Stack

- **Backend**: Django 4.2, Django REST Framework
- **Database**: MySQL 8.0
- **Cache**: Redis
- **Search**: Elasticsearch (optional)
- **Queue**: Celery with Redis broker
- **Storage**: AWS S3
- **Containerization**: Docker & Docker Compose

## Quick Start

### Prerequisites

- Python 3.11+
- MySQL 8.0
- Redis
- Docker (optional)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd nal-backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Database setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

### Docker Setup

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Run migrations**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

3. **Create superuser**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

## API Documentation

- **Swagger UI**: http://localhost:8000/api/docs/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

## Key Endpoints

### Authentication
- `POST /api/v1/auth/login/` - User login
- `POST /api/v1/auth/register/` - User registration
- `POST /api/v1/auth/refresh/` - Refresh token
- `POST /api/v1/auth/logout/` - Logout

### Properties
- `GET /api/v1/properties/` - List properties (with search/filters)
- `POST /api/v1/properties/create/` - Create property
- `GET /api/v1/properties/{id}/` - Get property details
- `PUT /api/v1/properties/{id}/update/` - Update property

### Documents
- `POST /api/v1/documents/upload-url/` - Get upload URL
- `POST /api/v1/documents/create/` - Create document record
- `GET /api/v1/documents/` - List documents
- `POST /api/v1/documents/{id}/verify/` - Verify document

### Bookings
- `POST /api/v1/bookings/create/` - Create booking
- `GET /api/v1/bookings/` - List bookings
- `GET /api/v1/bookings/slots/{property_id}/` - Get available slots

### Payments
- `POST /api/v1/payments/initiate/` - Initiate payment
- `POST /api/v1/payments/{id}/confirm/` - Confirm payment
- `POST /api/v1/payments/webhooks/razorpay/` - Payment webhook

## Architecture

### Core Apps

1. **Authentication** - User management and JWT authentication
2. **Users** - User profiles and audit logging
3. **Properties** - Property listings and media management
4. **Documents** - Document upload and verification pipeline
5. **Payments** - Payment processing and transaction management
6. **Bookings** - Appointment scheduling system
7. **Notifications** - Multi-channel notification system
8. **Analytics** - Analytics and reporting
9. **Admin Panel** - Administrative interface

### Background Tasks

- Document OCR processing
- ML-based verification
- Email/SMS notifications
- Search index synchronization
- Analytics data processing

## Security Features

- JWT authentication with refresh token rotation
- Role-based access control (RBAC)
- Input validation and sanitization
- SQL injection prevention
- XSS protection
- CSRF protection
- Rate limiting
- Secure file uploads with virus scanning
- Encrypted sensitive data storage

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=nal_backend

# Run specific test file
pytest nal_backend/apps/authentication/tests.py

# Run with markers
pytest -m "not slow"
```

## Deployment

### AWS Infrastructure

1. **Setup Terraform**
   ```bash
   cd infrastructure
   terraform init
   terraform plan
   terraform apply
   ```

2. **Deploy with CI/CD**
   - Push to main branch triggers automatic deployment
   - GitHub Actions handles testing, building, and deployment

### Environment Variables

Key environment variables for production:

```bash
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DB_HOST=your-rds-endpoint
REDIS_URL=redis://your-elasticache-endpoint:6379
AWS_STORAGE_BUCKET_NAME=your-s3-bucket
```

## Monitoring & Observability

- **Metrics**: Prometheus + Grafana
- **Logging**: Structured JSON logs
- **Tracing**: OpenTelemetry + Jaeger
- **Health Checks**: `/health/` endpoint
- **Error Tracking**: Sentry integration

## Performance Optimization

- Database query optimization with select_related/prefetch_related
- Redis caching for frequently accessed data
- CDN for static/media files
- Database connection pooling
- Async task processing with Celery
- Elasticsearch for fast search

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Email: support@nalindia.com
- Documentation: https://docs.nalindia.com
- Issues: GitHub Issues