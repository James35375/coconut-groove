"""WSGI entry point.

Gunicorn loads `app` from this file in production.
For local dev, you can also `python wsgi.py` to run the Flask dev server.
"""
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
