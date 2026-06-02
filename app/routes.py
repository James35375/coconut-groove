"""Routes for Coconut Groove.

For now: just a landing page and a health check. Real flows come later.
"""
from flask import Blueprint, render_template, jsonify

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/health")
def health():
    """Simple liveness check — used by uptime monitors and deploy verification."""
    return jsonify(status="ok")
