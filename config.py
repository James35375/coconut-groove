"""Configuration for Coconut Grove.

Loads from environment variables (.env in dev, real env vars in prod).
Different config classes for development vs production.
"""
import os
from dotenv import load_dotenv

# Load .env in development. In production, env vars come from systemd.
load_dotenv()


class Config:
    """Base config — values shared across environments."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-do-not-use-in-prod")

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # DigitalOcean Spaces
    SPACES_ENDPOINT = os.environ.get("SPACES_ENDPOINT")
    SPACES_REGION = os.environ.get("SPACES_REGION", "nyc3")
    SPACES_BUCKET = os.environ.get("SPACES_BUCKET")
    SPACES_KEY = os.environ.get("SPACES_KEY")
    SPACES_SECRET = os.environ.get("SPACES_SECRET")
    SPACES_CDN_ENDPOINT = os.environ.get("SPACES_CDN_ENDPOINT")

    # Stripe
    STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY")
    STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
    STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET")

    # SendGrid
    SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
    SENDGRID_FROM_EMAIL = os.environ.get("SENDGRID_FROM_EMAIL")


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

    # Belt-and-suspenders: refuse to start in prod without a real SECRET_KEY
    @classmethod
    def validate(cls):
        if cls.SECRET_KEY == "dev-only-do-not-use-in-prod":
            raise RuntimeError("SECRET_KEY must be set in production.")
        if not cls.SQLALCHEMY_DATABASE_URI:
            raise RuntimeError("DATABASE_URL must be set in production.")


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
