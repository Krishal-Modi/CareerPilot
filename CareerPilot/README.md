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

## Deploy on Render + Neon (step by step)

This project is ready to deploy with:
- Render for hosting
- Neon PostgreSQL for production database

### 1. Push project to GitHub

From project root:

```powershell
git add .
git commit -m "Prepare deployment to Render with Neon"
git push origin main
```

### 2. Create Neon database

1. Sign in to Neon and create a project.
2. Create a database (or use the default one).
3. Open Neon connection details and copy:
	 - Host
	 - Database name
	 - User
	 - Password
	 - Port

Use the pooled host when available (better for serverless/web workloads).

### 3. Create a Render Web Service

1. Sign in to Render.
2. Click New -> Web Service.
3. Connect your GitHub repo.
4. Select branch (for example: main).
5. Render will read render.yaml automatically.

If you configure manually, use:
- Build command: `pip install -r requirements.txt; python manage.py collectstatic --noinput; python manage.py migrate`
- Start command: `gunicorn config.wsgi:application`

### 4. Add environment variables in Render

In Render service settings, add:

- `DJANGO_SECRET_KEY` = long random secret
- `DJANGO_DEBUG` = `False`
- `DJANGO_ALLOWED_HOSTS` = your Render host and custom domain (comma-separated)
	- Example: `careerpilot.onrender.com,www.yourdomain.com`
- `DJANGO_CSRF_TRUSTED_ORIGINS` = full https origins (comma-separated)
	- Example: `https://careerpilot.onrender.com,https://www.yourdomain.com`
- `POSTGRES_DB` = Neon database name
- `POSTGRES_USER` = Neon user
- `POSTGRES_PASSWORD` = Neon password
- `POSTGRES_HOST` = Neon host
- `POSTGRES_PORT` = `5432`
- `POSTGRES_SSLMODE` = `require`

### 5. First deploy

1. Trigger deploy in Render.
2. Open Deploy logs and confirm:
	 - dependencies installed
	 - collectstatic succeeded
	 - migrate succeeded
	 - gunicorn started

### 6. Create superuser (optional)

In Render shell:

```bash
python manage.py createsuperuser
```

### 7. Automatic updates from GitHub

Render auto-deploys by default when you push to the connected branch.

Workflow:
1. make code change
2. commit
3. push to GitHub
4. Render redeploys automatically

### 8. Data migration from local SQLite to Neon (optional)

If you want to move local data:

```powershell
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission > data.json
```

Then on Render shell (connected to Neon):

```bash
python manage.py loaddata data.json
```

### 9. Reliability notes

- SQLite is good for local development.
- Use Neon PostgreSQL in production for reliability and scaling.
- Free Render can sleep on inactivity; paid plan is better for always-on uptime.