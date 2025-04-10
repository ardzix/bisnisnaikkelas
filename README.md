# Bisnis Naik Kelas

A SaaS platform helping Indonesian SMEs assess their business readiness to "naik kelas" (level up).

## Features

- Business readiness assessment form
- Automated scoring and classification
- Asynchronous PDF report generation
- Business level classification (Micro, Small, Medium, Large)
- Customized recommendations based on assessment

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

## Development

- Main app: `readiness/`
- Models: `readiness/models.py`
- Views: `readiness/views.py`
- Background tasks: `readiness/tasks.py`
- Scoring logic: `readiness/scoring.py`

## Testing

Run tests with:
```bash
python manage.py test
```

## License

Proprietary - All rights reserved 