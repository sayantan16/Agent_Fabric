# flask_app/app.py
"""
Main Flask Application - FIXED VERSION
Entry point for the Agentic Fabric web interface
"""

import json
import os
import sys
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS

# Add project root to Python path for backend imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Import UI configuration
from flask_app.config_ui import config


def create_app(config_name=None):
    """
    Application factory pattern for Flask app creation.

    Args:
        config_name: Configuration environment ('development', 'production')

    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)

    # Determine configuration
    config_name = config_name or os.environ.get("FLASK_ENV", "development")
    app.config.from_object(config[config_name])

    # Enable CORS for API endpoints
    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": "*",
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": [
                    "Content-Type",
                    "Authorization",
                    "HX-Request",
                    "HX-Target",
                ],
            }
        },
    )

    # Ensure upload directory exists
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(app.config["OUTPUT_FOLDER"], exist_ok=True)

    # Initialize extensions and register blueprints
    register_blueprints(app)
    register_error_handlers(app)
    register_template_functions(app)

    # FIXED: Use proper Flask 3.0 initialization method instead of before_first_request
    with app.app_context():
        initialize_services()

    return app


def initialize_services():
    """Initialize services at application startup (Flask 3.0 compatible)."""
    try:
        from flask_app.services import (
            orchestrator_service,
            registry_service,
            workflow_service,
        )

        print("DEBUG: Initializing services...")

        # Initialize orchestrator service with sample data
        if orchestrator_service.is_backend_available():
            orchestrator_service.create_sample_workflows()
            print("DEBUG: Orchestrator service initialized successfully")
        else:
            print("WARNING: Orchestrator service not available")

        print("DEBUG: Services initialization completed")

    except Exception as e:
        print(f"ERROR: Failed to initialize services: {e}")


def register_blueprints(app):
    """Register Flask blueprints for route organization."""
    try:
        from flask_app.routes.main import main_bp
        from flask_app.routes.api import api_bp

        app.register_blueprint(main_bp)
        app.register_blueprint(api_bp, url_prefix="/api")

    except ImportError as e:
        app.logger.warning(f"Blueprint import failed: {e}")


def register_error_handlers(app):
    """Register custom error handlers."""

    @app.errorhandler(404)
    def not_found_error(error):
        return (
            render_template(
                "error.html", error_code=404, error_message="Page not found"
            ),
            404,
        )

    @app.errorhandler(500)
    def internal_error(error):
        return (
            render_template(
                "error.html", error_code=500, error_message="Internal server error"
            ),
            500,
        )

    @app.errorhandler(413)
    def file_too_large(error):
        return (
            jsonify(
                {
                    "error": "File too large",
                    "message": f'Maximum file size is {app.config["MAX_CONTENT_LENGTH"] // (1024*1024)}MB',
                }
            ),
            413,
        )


def register_template_functions(app):
    """Register custom template functions and filters."""

    @app.template_filter("file_size")
    def file_size_filter(size_bytes):
        """Convert bytes to human readable format."""
        if size_bytes == 0:
            return "0 B"

        size_names = ["B", "KB", "MB", "GB"]
        import math

        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_names[i]}"

    @app.template_filter("time_ago")
    def time_ago_filter(timestamp):
        """Convert timestamp to relative time."""
        from datetime import datetime

        if isinstance(timestamp, str):
            try:
                timestamp = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            except:
                return timestamp

        now = datetime.now(timestamp.tzinfo if timestamp.tzinfo else None)
        diff = now - timestamp

        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days != 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        else:
            return "just now"

    @app.context_processor
    def inject_globals():
        """Inject global variables into all templates."""
        return {
            "app_name": "Agentic Fabric",
            "app_version": "1.0.0",
            "debug_mode": app.config.get("ENABLE_DEBUG_MODE", False),
            "show_code_gen": app.config.get("SHOW_CODE_GENERATION", False),
        }


# Create app instance
app = create_app()


@app.route("/favicon.ico")
def favicon():
    """Handle favicon requests to prevent 404 errors."""
    from flask import send_from_directory

    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@app.route("/test-backend")
def test_backend():
    """Test backend integration."""
    from flask_app.services import (
        orchestrator_service,
        registry_service,
        workflow_service,
    )

    # Test services
    results = {
        "orchestrator_available": orchestrator_service.is_backend_available(),
        "registry_available": registry_service.is_available(),
        "workflow_available": workflow_service.is_available(),
        "registry_stats": (
            registry_service.get_registry_stats()
            if registry_service.is_available()
            else {}
        ),
        "agents_count": (
            len(registry_service.get_agents_list())
            if registry_service.is_available()
            else 0
        ),
        "tools_count": (
            len(registry_service.get_tools_list())
            if registry_service.is_available()
            else 0
        ),
    }

    return f"""
    <h1>Backend Integration Test</h1>
    <pre>{json.dumps(results, indent=2)}</pre>
    <a href="/">← Back to main</a>
    """


if __name__ == "__main__":
    # Development server
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host="127.0.0.1", port=port, debug=app.config.get("DEBUG", True), threaded=True
    )
