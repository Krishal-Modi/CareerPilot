# CareerPilot

Phase 1 of a Django job application tracker.

## Local setup

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe manage.py migrate
.venv\Scripts\python.exe manage.py runserver
```

Open <http://127.0.0.1:8000/>. Register a user, then log in. The dashboard requires authentication and currently uses SQLite until `POSTGRES_DB` is set.

## PostgreSQL / Supabase

Use `.env.example` as a reference and provide the PostgreSQL values in your process environment. Django reads `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT`, and `POSTGRES_SSLMODE`; it does not load `.env` files automatically. In production, also set a strong `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, and `DJANGO_ALLOWED_HOSTS`.

PowerShell example:

```powershell
$env:DJANGO_SECRET_KEY = 'use-a-generated-secret'
$env:DJANGO_DEBUG = 'False'
$env:POSTGRES_DB = 'postgres'
$env:POSTGRES_USER = 'postgres.your-project-ref'
$env:POSTGRES_PASSWORD = 'your-password'
$env:POSTGRES_HOST = 'your-pooler-host'
$env:POSTGRES_PORT = '5432'
$env:POSTGRES_SSLMODE = 'require'
python manage.py migrate
```

Password reset and profile pages will be added in the next authentication increment before application data is introduced.