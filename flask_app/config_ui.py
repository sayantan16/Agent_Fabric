# flask_app/config_ui.py
"""
Flask UI Configuration
Separate from core config.py to avoid conflicts
"""

import os
from datetime import timedelta


class Config:
    """Base configuration class."""

    # Flask Core Settings
    SECRET_KEY = (
        os.environ.get("FLASK_SECRET_KEY")
        or "agentic-fabric-dev-key-change-in-production"
    )

    # Upload Settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
    ALLOWED_EXTENSIONS = {
        "txt",
        "pdf",
        "csv",
        "json",
        "xlsx",
        "xls",
        "docx",
        "jpg",
        "jpeg",
        "png",
    }

    # Session Settings
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)

    # HTMX Settings
    HTMX_BOOSTED = True

    # Backend Integration
    BACKEND_TIMEOUT = 30  # seconds
    MAX_WORKFLOW_TIME = 300  # 5 minutes max per workflow

    # UI Settings
    ITEMS_PER_PAGE = 20
    ENABLE_DEBUG_MODE = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    SHOW_CODE_GENERATION = os.environ.get("SHOW_CODE_GEN", "False").lower() == "true"

    # Real-time Updates
    SSE_HEARTBEAT_INTERVAL = 30  # seconds
    WORKFLOW_POLL_INTERVAL = 1  # seconds


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True
    EXPLAIN_TEMPLATE_LOADING = False


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False
    TESTING = False


# Configuration mapping
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
