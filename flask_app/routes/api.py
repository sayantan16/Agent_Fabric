# flask_app/routes/api.py
"""
API Routes Blueprint
Handles AJAX requests, file uploads, and data endpoints
"""

import os
import json
import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app, session
from werkzeug.utils import secure_filename
from flask_app.services.orchestrator_service import orchestrator_service
from flask_app.services.registry_service import registry_service
from flask_app.services.workflow_service import workflow_service

api_bp = Blueprint("api", __name__)


def allowed_file(filename):
    """Check if file extension is allowed."""
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["ALLOWED_EXTENSIONS"]
    )


@api_bp.route("/health")
def health_check():
    """System health check endpoint."""
    try:
        health_data = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "services": {
                "orchestrator": orchestrator_service.is_backend_available(),
                "registry": registry_service.is_available(),
                "workflow": workflow_service.is_available(),
            },
            "system_stats": orchestrator_service.get_system_stats(),
            "version": "1.0.0",
        }

        # Determine overall health
        all_services_up = all(health_data["services"].values())
        health_data["status"] = "healthy" if all_services_up else "degraded"

        status_code = 200 if all_services_up else 503
        return jsonify(health_data), status_code

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "unhealthy",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat(),
                }
            ),
            500,
        )


@api_bp.route("/upload", methods=["POST"])
def upload_file():
    """Handle file uploads."""
    try:
        if "files" not in request.files:
            return jsonify({"error": "No files provided"}), 400

        files = request.files.getlist("files")
        uploaded_files = []

        for file in files:
            if file.filename == "":
                continue

            if file and allowed_file(file.filename):
                # Generate unique filename
                filename = secure_filename(file.filename)
                unique_id = uuid.uuid4().hex[:8]
                name, ext = os.path.splitext(filename)
                unique_filename = f"{name}_{unique_id}{ext}"

                # Save file
                filepath = os.path.join(
                    current_app.config["UPLOAD_FOLDER"], unique_filename
                )
                file.save(filepath)

                # Get file metadata
                file_stats = os.stat(filepath)

                file_metadata = {
                    "id": unique_id,
                    "original_name": filename,
                    "stored_name": unique_filename,
                    "path": filepath,
                    "size": file_stats.st_size,
                    "type": file.content_type or "application/octet-stream",
                    "uploaded_at": datetime.now().isoformat(),
                }

                uploaded_files.append(file_metadata)
            else:
                return (
                    jsonify({"error": f"File type not allowed: {file.filename}"}),
                    400,
                )

        return jsonify(
            {"status": "success", "files": uploaded_files, "count": len(uploaded_files)}
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/process", methods=["POST"])
def process_request():
    """Main request processing endpoint."""
    try:
        data = request.get_json()

        if not data or "request" not in data:
            return jsonify({"error": "No request text provided"}), 400

        request_text = data["request"].strip()
        if not request_text:
            return jsonify({"error": "Request text cannot be empty"}), 400

        # Get processing options from request or session
        auto_create = data.get("auto_create", session.get("auto_create", True))
        workflow_type = data.get(
            "workflow_type", session.get("workflow_type", "sequential")
        )
        files = data.get("files", [])

        # Process request asynchronously
        import asyncio

        result = asyncio.run(
            orchestrator_service.process_user_request(
                request_text=request_text,
                files=files,
                auto_create=auto_create,
                workflow_type=workflow_type,
            )
        )

        return jsonify(result)

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "error": str(e),
                    "message": "Request processing failed",
                }
            ),
            500,
        )


@api_bp.route("/workflow/<workflow_id>/status")
def get_workflow_status(workflow_id):
    """Get current status of a workflow."""
    try:
        status = orchestrator_service.get_workflow_status(workflow_id)

        if not status:
            return jsonify({"error": "Workflow not found"}), 404

        return jsonify(status)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/workflow/<workflow_id>/cancel", methods=["DELETE"])
def cancel_workflow(workflow_id):
    """Cancel an active workflow."""
    try:
        success = orchestrator_service.cancel_workflow(workflow_id)

        if success:
            return jsonify({"status": "cancelled", "workflow_id": workflow_id})
        else:
            return jsonify({"error": "Workflow not found or already completed"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/workflow/<workflow_id>/stream")
def stream_workflow_updates(workflow_id):
    """Stream real-time workflow updates via Server-Sent Events."""
    try:

        def generate():
            yield "data: " + json.dumps(
                {
                    "type": "connection",
                    "message": "Connected to workflow stream",
                    "workflow_id": workflow_id,
                }
            ) + "\n\n"

            # Stream updates from workflow service
            for update in workflow_service.stream_workflow_updates(workflow_id):
                yield update

        return current_app.response_class(
            generate(),
            mimetype="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
            },
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/workflows")
def list_workflows():
    """Get list of workflows with pagination."""
    try:
        page = int(request.args.get("page", 1))
        per_page = min(int(request.args.get("per_page", 20)), 100)  # Max 100 per page

        all_workflows = orchestrator_service.get_workflow_history()
        active_workflows = orchestrator_service.get_active_workflows()

        # Simple pagination
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        workflows = all_workflows[start_idx:end_idx]

        return jsonify(
            {
                "workflows": workflows,
                "active_workflows": active_workflows,
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": len(all_workflows),
                    "pages": (len(all_workflows) + per_page - 1) // per_page,
                },
                "stats": orchestrator_service.get_system_stats(),
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/registry/agents")
def list_agents():
    """Get list of available agents."""
    try:
        tags = request.args.getlist("tags")
        active_only = request.args.get("active_only", "true").lower() == "true"

        agents = registry_service.get_agents_list(
            tags=tags if tags else None, active_only=active_only
        )

        return jsonify({"agents": agents, "count": len(agents)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/registry/tools")
def list_tools():
    """Get list of available tools."""
    try:
        tags = request.args.getlist("tags")
        pure_only = request.args.get("pure_only", "false").lower() == "true"

        tools = registry_service.get_tools_list(
            tags=tags if tags else None, pure_only=pure_only
        )

        return jsonify({"tools": tools, "count": len(tools)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/registry/stats")
def registry_stats():
    """Get registry statistics."""
    try:
        stats = registry_service.get_registry_stats()
        return jsonify(stats)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/registry/search")
def search_registry():
    """Search agents and tools."""
    try:
        query = request.args.get("q", "").strip()

        if not query:
            return jsonify({"error": "Query parameter 'q' is required"}), 400

        results = registry_service.search_components(query)
        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/registry/dependencies")
def get_dependencies():
    """Get dependency graph data."""
    try:
        graph = registry_service.get_dependency_graph()
        return jsonify(graph)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/test-connection")
def test_connection():
    """Test backend connectivity."""
    try:
        results = {
            "timestamp": datetime.now().isoformat(),
            "services": {
                "orchestrator": {
                    "available": orchestrator_service.is_backend_available(),
                    "stats": orchestrator_service.get_system_stats(),
                },
                "registry": {
                    "available": registry_service.is_available(),
                    "stats": registry_service.get_registry_stats(),
                },
                "workflow": {"available": workflow_service.is_available()},
            },
        }

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Error handlers for API routes
@api_bp.errorhandler(400)
def bad_request(error):
    """Handle 400 errors in API."""
    return jsonify({"error": "Bad request", "message": str(error)}), 400


@api_bp.errorhandler(404)
def not_found_api(error):
    """Handle 404 errors in API."""
    return jsonify({"error": "Endpoint not found"}), 404


@api_bp.errorhandler(500)
def internal_error_api(error):
    """Handle 500 errors in API."""
    return jsonify({"error": "Internal server error"}), 500


@api_bp.route("/chat/message", methods=["POST"])
def send_chat_message():
    """Process a chat message with full workflow tracking."""
    try:
        data = request.get_json()

        if not data or "message" not in data:
            return jsonify({"error": "No message provided"}), 400

        message = data["message"].strip()
        if not message:
            return jsonify({"error": "Message cannot be empty"}), 400

        files = data.get("files", [])
        settings = data.get("settings", {})

        # Get user preferences
        auto_create = settings.get("auto_create", session.get("auto_create", True))
        workflow_type = settings.get(
            "workflow_type", session.get("workflow_type", "sequential")
        )

        # Generate unique message ID for tracking
        import uuid

        message_id = f"msg_{uuid.uuid4().hex[:8]}"

        # Store message in session for persistence
        if "chat_history" not in session:
            session["chat_history"] = []

        session["chat_history"].append(
            {
                "id": message_id,
                "message": message,
                "timestamp": datetime.now().isoformat(),
                "type": "user",
                "files": files,
            }
        )

        # Process through orchestrator
        import asyncio

        result = asyncio.run(
            orchestrator_service.process_user_request(
                request_text=message,
                files=files,
                auto_create=auto_create,
                workflow_type=workflow_type,
            )
        )

        # Add system response to chat history
        system_response = {
            "id": f"sys_{uuid.uuid4().hex[:8]}",
            "message": result.get("response", "Request processed"),
            "timestamp": datetime.now().isoformat(),
            "type": "system",
            "workflow_id": result.get("workflow_id"),
            "status": result.get("status"),
            "metadata": {
                "agents_used": result.get("workflow", {}).get("steps", []),
                "execution_time": result.get("execution_time", 0),
                "components_created": result.get("metadata", {}).get(
                    "components_created", 0
                ),
            },
        }

        session["chat_history"].append(system_response)
        session.modified = True

        return jsonify(
            {
                "status": "success",
                "message_id": message_id,
                "response": system_response,
                "workflow_data": result,
                "chat_updated": True,
            }
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "error": str(e),
                    "message": "Failed to process message",
                }
            ),
            500,
        )


@api_bp.route("/chat/history")
def get_chat_history():
    """Get current chat history."""
    try:
        history = session.get("chat_history", [])
        return jsonify({"history": history, "count": len(history)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/chat/clear", methods=["POST"])
def clear_chat_history():
    """Clear chat history."""
    try:
        session["chat_history"] = []
        session.modified = True
        return jsonify({"status": "success", "message": "Chat history cleared"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/chat/export")
def export_chat_history():
    """Export chat history as JSON."""
    try:
        history = session.get("chat_history", [])

        export_data = {
            "exported_at": datetime.now().isoformat(),
            "message_count": len(history),
            "session_id": session.get("session_id", "unknown"),
            "messages": history,
        }

        from flask import make_response

        response = make_response(json.dumps(export_data, indent=2))
        response.headers["Content-Type"] = "application/json"
        response.headers["Content-Disposition"] = (
            f'attachment; filename=chat_history_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        )

        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/workflow/<workflow_id>/visualization")
def get_workflow_visualization(workflow_id):
    """Get workflow visualization data."""
    try:
        viz_data = workflow_service.get_workflow_visualization(workflow_id)
        return jsonify(viz_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/files/<file_id>/preview")
def get_file_preview(file_id):
    """Get file preview data."""
    try:
        # This would implement file preview logic
        # For now, return placeholder
        return jsonify(
            {
                "file_id": file_id,
                "preview": "File preview not yet implemented",
                "type": "text",
                "size": 0,
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
