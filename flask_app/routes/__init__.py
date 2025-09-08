# flask_app/routes/__init__.py
"""
Route Blueprints for Flask Application
Organized by functionality: main, api, orchestrator, registry
"""

from .main import main_bp
from .api import api_bp

__all__ = ["main_bp", "api_bp"]
