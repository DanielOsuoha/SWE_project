# SWE_project

A Django-based web application.

## Prerequisites

- Python 3.8+
- pip
- virtualenv (recommended)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/SWE_project.git
cd SWE_project
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up database:
```bash
python manage.py migrate
```

## Running the Application

1. Start the development server:
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000`

## Development

Create a superuser to access the admin interface:
```bash
python manage.py createsuperuser
```

Run tests:
```bash
python manage.py test
```

Collect static files:
```bash
python manage.py collectstatic
```

## License

[MIT](LICENSE)
