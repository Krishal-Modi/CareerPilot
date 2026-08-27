# CareerPilot

Phase 1 of a Django job application tracker.

## Local setup

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe manage.py migrate
.venv\Scripts\python.exe manage.py runserver
```

Open <http://127.0.0.1:8000/>. Register a user, then log in. Firebase Authentication stores accounts and Firestore stores applications and referrals.

## Deploy on Render + Firebase (step by step)

This project uses Render for hosting and Firebase Authentication plus Cloud Firestore for data. Existing Neon data is not imported.

### 1. Push project to GitHub

From project root:

```powershell
git add .
git commit -m "Prepare deployment to Render with Neon"
git push origin main
```

### 2. Create Firebase project

1. Sign in to the Firebase Console with any Google account.
2. Create a project.
3. Open Authentication -> Sign-in method and enable Email/Password.
4. Open Firestore Database -> Create database and choose Production mode.
5. Open Project settings -> General and copy the Web API key.
6. Open Project settings -> Service accounts -> Generate new private key.
7. Keep the downloaded JSON private. Never commit it to GitHub.

The Firebase account may be different from your GitHub or Render account.

### 3. Create a Render Web Service

1. Sign in to Render.
2. Click New -> Web Service.
3. Connect your GitHub repo.
4. Select branch (for example: main).
5. Render will read render.yaml automatically.

If you configure manually, use:
- Build command: `pip install -r requirements.txt; python manage.py collectstatic --noinput`
- Start command: `gunicorn config.wsgi:application`

### 4. Add environment variables in Render

In Render service settings, add:

- `DJANGO_SECRET_KEY` = long random secret
- `DJANGO_DEBUG` = `False`
- `DJANGO_ALLOWED_HOSTS` = your Render host and custom domain (comma-separated)
	- Example: `careerpilot.onrender.com,www.yourdomain.com`
- `DJANGO_CSRF_TRUSTED_ORIGINS` = full https origins (comma-separated)
	- Example: `https://careerpilot.onrender.com,https://www.yourdomain.com`
- `FIREBASE_WEB_API_KEY` = Firebase Web API key
- `FIREBASE_CREDENTIALS_JSON_BASE64` = base64-encoded contents of the downloaded service-account JSON (recommended; use this instead of `FIREBASE_CREDENTIALS_JSON`)

To create the base64 value in PowerShell without changing the JSON file:

```powershell
[Convert]::ToBase64String([IO.File]::ReadAllBytes('firebase-service-account.json'))
```

Copy the output into Render as `FIREBASE_CREDENTIALS_JSON_BASE64`. Do not commit the JSON file or the encoded value. The app also accepts the complete JSON in `FIREBASE_CREDENTIALS_JSON` if base64 is not used.

### 5. First deploy

1. Trigger deploy in Render.
2. Open Deploy logs and confirm:
	 - dependencies installed
	 - collectstatic succeeded
	 - gunicorn started

### 6. Automatic updates from GitHub

Render auto-deploys by default when you push to the connected branch.

Workflow:
1. make code change
2. commit
3. push to GitHub
4. Render redeploys automatically

### 7. Reliability notes

- Firestore stores each application in `applications` and referrals in its `referrals` subcollection.
- Firebase UID ownership prevents users from viewing each other's applications.
- Free Render can sleep on inactivity; paid plan is better for always-on uptime.