# Coconut Grove

Custom engraved coconuts — public-facing e-commerce site with AI-generated designs.

## Stack
- Flask + SQLAlchemy + Flask-Migrate
- PostgreSQL (DigitalOcean Managed)
- Gunicorn + Nginx (production)
- DigitalOcean Spaces (object storage)
- Stripe Checkout (payments)
- SendGrid (transactional email)

## Local development (Windows / PowerShell)

```powershell
# Clone
git clone git@github.com:<you>/coconut-grove.git
cd coconut-grove

# Virtual env
python -m venv venv
.\venv\Scripts\Activate.ps1

# Dependencies
pip install -r requirements.txt

# Environment variables
Copy-Item .env.example .env
# then edit .env with real values (DB connection string, etc.)

# Initialize the database (first time only)
$env:FLASK_APP = "wsgi.py"
flask db init
flask db migrate -m "initial"
flask db upgrade

# Run
python wsgi.py
```

Visit http://127.0.0.1:5000

## Project structure

```
coconut-grove/
├── app/
│   ├── __init__.py       # Flask app factory
│   ├── routes.py         # URL routes
│   ├── models.py         # SQLAlchemy models
│   └── templates/        # Jinja templates
├── config.py             # Config classes (dev/prod)
├── wsgi.py               # Entry point
├── requirements.txt
├── .env.example          # Template — copy to .env
└── .gitignore
```

## Deployment

Deployed to a DigitalOcean droplet (NYC3) via SSH + git pull + systemd.
See `docs/deploy.md` (TBD).
