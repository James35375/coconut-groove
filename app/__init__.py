"""Flask application factory.

Standard pattern: create_app() builds and configures a Flask instance.
Lets us instantiate the app with different configs for dev/test/prod.
"""
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import config

# Extensions instantiated here, bound to the app inside create_app().
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name: str | None = None) -> Flask:
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "default")

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    if config_name == "production":
        config[config_name].validate()

    # Bind extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)

    return app
