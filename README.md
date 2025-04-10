# Bisnis Naik Kelas

A SaaS platform helping Indonesian SMEs assess their business readiness to "naik kelas" (level up).

## Features

- Business readiness assessment form
- Level-aware, weighted scoring system
- Automated business classification (Micro, Small, Medium, Large)
- Customized recommendations based on business level
- Asynchronous PDF report generation
- Comprehensive assessment across multiple business dimensions

## Project Structure

- **readiness/**: Main application
  - **models.py**: Database models for assessments and questions
  - **views.py**: Request handlers and business logic
  - **scoring.py**: Level-aware scoring algorithm
  - **tasks.py**: Background tasks for report generation
  - **constants.py**: Business level definitions and scoring weights
  - **templates/**: HTML templates for forms and reports
  - **admin.py**: Django admin interface configuration

## Scoring System

The platform uses a sophisticated, level-aware scoring system that:

- Classifies businesses into Micro, Small, Medium, or Large based on revenue and employee count
- Applies different weighted criteria for each business level
- Evaluates readiness across multiple dimensions:
  - Digital presence
  - Financial management
  - Legal compliance
  - Operational efficiency
  - Strategic planning
  - Risk management
  - Technology adoption
  - Market access
  - Process maturity

## Setup

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

4. Set up the database:
```bash
python manage.py migrate
```

5. Start Redis (required for background tasks):
```bash
redis-server
```

6. Run the development server:
```bash
python manage.py runserver
```

7. Start the background task worker:
```bash
python manage.py qcluster
```

8. Collect static files:
```bash
python manage.py collectstatic
```

## Development

### Key Components

- **Business Assessment**: Captures business information and readiness indicators
- **Scoring Algorithm**: Determines business level and calculates readiness scores
- **Recommendation Engine**: Generates tailored suggestions based on assessment results
- **PDF Report Generator**: Creates detailed assessment reports asynchronously

### Code Organization

- **Models**: Define data structure and relationships
- **Views**: Handle HTTP requests and form processing
- **Tasks**: Manage background processing for report generation
- **Templates**: Render HTML for forms and reports

## Testing

Run tests with:
```bash
python manage.py test
```

## Deployment

For production deployment:

1. Set `DEBUG = False` in settings.py
2. Configure a production database
3. Set up a web server (e.g., Nginx, Apache)
4. Configure static and media file serving
5. Set up SSL/TLS for secure connections
6. Configure environment variables for production

## License

Proprietary - All rights reserved 