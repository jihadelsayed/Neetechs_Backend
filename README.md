# Neetechs Backend

Django backend for the Neetechs platform. Provides APIs for auth, profiles, services, categories, checkout/payments, chat (WebSockets via Channels), and more.

- **Domain:** `server.neetechs.com`
- **Prod paths:** app: `/srv/neetechs/app`, venv: `/srv/neetechs/env`
- **Service:** `gunicorn-neetechs` (systemd)
- **DB:** PostgreSQL
- **Static root:** `/srv/neetechs/app/staticfiles`
- **Contact:** info@neetechs.com

## Tech Stack
- Django, Django REST Framework
- Django Channels (ASGI websockets)
- django-allauth (email login)
- Knox tokens (or DRF tokens), CORS headers
- PostgreSQL (psycopg)
- (Optional) S3 via django-storages/boto3

## Features (high level)
- Email-only authentication (allauth)
- User profiles
- Services/Categories catalog
- Checkout/Stripe integration
- Chat (Channels websockets)
- Admin dashboard

---

## Quick Start (Local)

### 1) Clone
```bash
git clone <repo-url>
cd neetechs-backend
```

### 2) Python env
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3) Configure environment
Copy and edit:
```bash
cp .env.example .env
```

**`.env.example`**
```env
# Django
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=http://127.0.0.1:8000,http://localhost:8000

# Database (either DATABASE_URL or individual fields)
DATABASE_URL=postgres://neetechs:neetechs@127.0.0.1:5432/neetechs
# Or:
DB_NAME=neetechs
DB_USER=neetechs
DB_PASSWORD=neetechs
DB_HOST=127.0.0.1
DB_PORT=5432

# CORS
CORS_ALLOWED_ORIGINS=http://127.0.0.1:4200,http://localhost:4200

# Email / Providers (adjust)
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=info@neetechs.com
EMAIL_HOST_PASSWORD=change-me
EMAIL_PORT=587
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=info@neetechs.com

# Stripe (if used)
STRIPE_SECRET_KEY=sk_live_or_test
STRIPE_PUBLIC_KEY=pk_live_or_test

# S3 (optional)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
AWS_S3_REGION_NAME=
```

### 4) DB setup (local example)
```bash
# Linux example
sudo -u postgres psql <<SQL
CREATE USER neetechs WITH PASSWORD 'neetechs';
CREATE DATABASE neetechs OWNER neetechs;
GRANT ALL PRIVILEGES ON DATABASE neetechs TO neetechs;
SQL
```

### 5) Migrate + run
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
# http://127.0.0.1:8000/
```

---

## Deployment (Linode + Nginx + Gunicorn)

### Paths/assumptions
- Code: `/srv/neetechs/app`
- Venv: `/srv/neetechs/env`
- System user: `deploy`
- Service: `gunicorn-neetechs`
- Domain: `server.neetechs.com`

### Gunicorn systemd unit
`/etc/systemd/system/gunicorn-neetechs.service`
```ini
[Unit]
Description=Gunicorn Neetechs
After=network.target

[Service]
User=deploy
Group=www-data
WorkingDirectory=/srv/neetechs/app
Environment="PATH=/srv/neetechs/env/bin"
EnvironmentFile=/srv/neetechs/app/.env
ExecStart=/srv/neetechs/env/bin/gunicorn config.asgi:application   --workers 3 --worker-class uvicorn.workers.UvicornWorker   --bind 127.0.0.1:8001 --timeout 120

Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now gunicorn-neetechs
```

### Nginx (reverse proxy)
`/etc/nginx/sites-available/neetechs.conf`
```nginx
server {
  server_name server.neetechs.com;

  client_max_body_size 25m;

  location /static/ {
    alias /srv/neetechs/app/staticfiles/;
  }

  location /media/ {
    alias /srv/neetechs/app/media/;
  }

  location / {
    proxy_pass http://127.0.0.1:8001;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_redirect off;
  }

  listen 80;
}
```

```bash
sudo ln -sf /etc/nginx/sites-available/neetechs.conf /etc/nginx/sites-enabled/neetechs.conf
sudo nginx -t && sudo systemctl reload nginx
```

### SSL (Let’s Encrypt)
```bash
sudo certbot --nginx -d server.neetechs.com --agree-tos -m info@neetechs.com -n
sudo systemctl restart nginx
```

### Static files (prod)
```bash
source /srv/neetechs/env/bin/activate
python /srv/neetechs/app/manage.py collectstatic --noinput
deactivate
```

---

## CI/CD (GitHub Actions → SSH deploy)

Secrets required:
- `SSH_HOST=server.neetechs.com`
- `SSH_USER=deploy`
- `SSH_KEY=<private key>`
- (optional) `SSH_PORT=22`

`.github/workflows/deploy.yml`
```yaml
name: Deploy Neetechs
on:
  push:
    branches: [ "main" ]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Add host
        run: |
          mkdir -p ~/.ssh
          ssh-keyscan -p "${{ secrets.SSH_PORT || 22 }}" -H "${{ secrets.SSH_HOST }}" >> ~/.ssh/known_hosts

      - name: Deploy over SSH
        uses: appleboy/ssh-action@v1.2.0
        with:
          host: ${{ secrets.SSH_HOST }}
          username: ${{ secrets.SSH_USER }}
          key: ${{ secrets.SSH_KEY }}
          port: ${{ secrets.SSH_PORT || 22 }}
          script: |
            sudo -u deploy -H bash <<'SH'
            set -Eeuo pipefail
            cd /srv/neetechs/app
            git pull

            source /srv/neetechs/env/bin/activate
            python -m pip install --upgrade -r requirements.linux.txt

            set -a
            source .env
            set +a

            python manage.py migrate --noinput -v 2
            python manage.py collectstatic --noinput
            deactivate
            SH

            sudo systemctl restart gunicorn-neetechs
            sudo systemctl is-active --quiet gunicorn-neetechs || (sudo journalctl -u gunicorn-neetechs -n 200 --no-pager && exit 1)
```

---

## Django Settings Notes

### Static config
```python
STATIC_URL = "/static/"
STATIC_ROOT = "/srv/neetechs/app/staticfiles"
# STATICFILES_DIRS = []  # only if you have extra local asset dirs
MEDIA_URL = "/media/"
MEDIA_ROOT = "/srv/neetechs/app/media"
```

### allauth (new API)
```python
ACCOUNT_LOGIN_METHODS = {"email"}  # replaces deprecated ACCOUNT_AUTHENTICATION_METHOD
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]  # replaces ACCOUNT_EMAIL_REQUIRED/USERNAME_REQUIRED
ACCOUNT_EMAIL_VERIFICATION = "mandatory"  # your choice
```

### Security (prod)
```python
DEBUG = False
ALLOWED_HOSTS = ["server.neetechs.com"]
CSRF_TRUSTED_ORIGINS = ["https://server.neetechs.com"]
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
```

---

## Common Commands

```bash
# Migrations
python manage.py makemigrations
python manage.py migrate -v 2

# Superuser
python manage.py createsuperuser

# Collect static
python manage.py collectstatic --noinput

# Run dev server
python manage.py runserver

# Health check (quick DB ping)
python - <<'PY'
import django; django.setup()
from django.db import connections
connections['default'].cursor().execute('SELECT 1'); print("DB OK")
PY
```

---

## Troubleshooting

- **Static warning**: “STATICFILES_DIRS path does not exist” → either create the dir or remove it; rely on `STATIC_ROOT` + `collectstatic`.
- **Postgres timeout**: check service `systemctl status postgresql`, `ss -lntp | grep 5432`, ensure Django `HOST=127.0.0.1` and credentials match. If remote DB, open UFW only to your app server IP and add proper `pg_hba.conf` entries.
- **allauth deprecations**: use `ACCOUNT_LOGIN_METHODS` and `ACCOUNT_SIGNUP_FIELDS` as shown above.
- **Gunicorn fails**: `journalctl -u gunicorn-neetechs -n 200 --no-pager`.

---

## License
Proprietary — Neetechs. All rights reserved.
