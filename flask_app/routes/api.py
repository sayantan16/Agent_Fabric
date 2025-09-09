# flask_app/routes/api.py - STREAMLINED VERSION
"""
API Routes Blueprint - Streamlined for Agentic Fabric POC
Handles AJAX requests, file uploads, and data endpoints
"""

import os
import json
from typing import Any, Dict
import uuid
from datetime import datetime
from flask import (
    Blueprint,
    request,
    jsonify,
    current_app,
    session,
    make_response,
    send_file,
)
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
        registry_stats = registry_service.get_registry_stats()

        # Ensure proper structure
        if not registry_stats or not registry_stats.get("available", False):
            registry_stats = {
                "available": False,
                "statistics": {"total_agents": 0, "total_tools": 0},
                "summary": {"health_score": 0, "status": "unavailable"},
            }

        health_data = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "services": {
                "orchestrator": orchestrator_service.is_backend_available(),
                "registry": {
                    "available": registry_stats.get("available", False),
                    "stats": registry_stats.get(
                        "statistics", {"total_agents": 0, "total_tools": 0}
                    ),
                    "health_score": registry_stats.get("summary", {}).get(
                        "health_score", 0
                    ),
                    "status": registry_stats.get("summary", {}).get(
                        "status", "unknown"
                    ),
                },
            },
            "system_stats": orchestrator_service.get_system_stats(),
            "version": "1.0.0",
        }

        # Determine overall health
        orchestrator_ok = health_data["services"]["orchestrator"]
        registry_ok = health_data["services"]["registry"]["available"]

        if orchestrator_ok and registry_ok:
            health_data["status"] = "healthy"
            status_code = 200
        elif orchestrator_ok or registry_ok:
            health_data["status"] = "degraded"
            status_code = 200
        else:
            health_data["status"] = "unhealthy"
            status_code = 503

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


@api_bp.route("/chat/message", methods=["POST"])
def send_chat_message():
    """Process a chat message with natural language support."""
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

        # Generate unique message ID
        message_id = f"msg_{uuid.uuid4().hex[:8]}"

        # Store in session
        if "chat_history" not in session:
            session["chat_history"] = []

        user_message = {
            "id": message_id,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "type": "user",
            "files": files,
        }
        session["chat_history"].append(user_message)

        # Process through orchestrator
        import asyncio

        try:
            result = asyncio.run(
                orchestrator_service.process_user_request(
                    request_text=message,
                    files=files,
                    auto_create=auto_create,
                    workflow_type=workflow_type,
                )
            )
        except Exception as e:
            result = {
                "status": "error",
                "error": str(e),
                "response": f"I encountered an error processing your request: {str(e)}",
            }

        # Create natural language response
        response_text = create_natural_response(result, message)

        # Add system response to session
        system_response = {
            "id": f"sys_{uuid.uuid4().hex[:8]}",
            "message": response_text,
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
                "workflow_type": workflow_type,
            },
        }

        session["chat_history"].append(system_response)
        session.modified = True

        return jsonify(
            {
                "status": "success",
                "message_id": message_id,
                "response": response_text,
                "workflow_id": result.get("workflow_id"),
                "workflow": result.get("workflow", {}),
                "execution_time": result.get("execution_time", 0),
                "results": result.get("results", {}),
                "metadata": system_response["metadata"],
                "chat_updated": True,
            }
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "error": str(e),
                    "response": f"I'm having technical difficulties: {str(e)}",
                }
            ),
            500,
        )


def create_natural_response(result, original_request):
    """Create response using orchestrator output or intelligent fallbacks."""

    # ALWAYS use the orchestrator's synthesized response first
    if result.get("response"):
        response = result["response"]
        print(f"DEBUG: Using orchestrator response: {response[:100]}...")

        # Enhanced: Format attribution nicely if present
        if "*Processed using" in response:
            # Split main response from attribution
            parts = response.split("*Processed using", 1)
            main_text = parts[0].strip()

            if len(parts) > 1:
                # Clean and format attribution
                attribution = "Processed using" + parts[1].replace("*", "").strip()
                # Add subtle styling with HTML
                formatted_response = f"{main_text}\n\n<small class='text-muted'><i class='fas fa-cogs'></i> {attribution}</small>"
                return formatted_response

        return response

    # IMPROVED: Use original_request for context-aware fallbacks
    if result.get("status") == "error":
        error_msg = result.get("error", "An unknown error occurred")
        return f"I encountered an error while processing your request '{original_request[:50]}...': {error_msg}"

    # IMPROVED: Context-aware partial response using original_request
    agent_count = len(result.get("workflow", {}).get("steps", []))
    if agent_count > 0:
        # Try to extract some meaning from results even without orchestrator synthesis
        basic_summary = extract_basic_results(
            result.get("results", {}), original_request
        )
        if basic_summary:
            # Enhanced: Add styled attribution to fallback responses
            agent_names = ", ".join(result.get("workflow", {}).get("steps", []))
            styled_attribution = f"<small class='text-muted'><i class='fas fa-cogs'></i> Processed using {agent_count} agent{'s' if agent_count != 1 else ''}: {agent_names}</small>"
            return f"{basic_summary}\n\n{styled_attribution}\n\n<em>(Detailed response generation failed)</em>"
        else:
            return f"I attempted to process '{original_request[:50]}...' using {agent_count} agent{'s' if agent_count != 1 else ''}, but couldn't generate a detailed response."
    else:
        return f"I couldn't determine how to handle your request: '{original_request[:50]}...'. Please provide more specific instructions."


def extract_basic_results(results, original_request):
    """Extract basic results when orchestrator synthesis fails."""
    if not results:
        return None

    request_lower = original_request.lower()
    basic_findings = []

    for agent_name, result in results.items():
        if isinstance(result, dict) and result.get("status") == "success":
            data = result.get("data", {})

            # Context-aware result extraction based on original request
            if "count" in request_lower and "word" in request_lower:
                if "word_count" in data:
                    return f"I counted {data['word_count']} words in your text."

            elif "extract" in request_lower and "email" in request_lower:
                if "emails" in data and data["emails"]:
                    count = len(data["emails"])
                    return f"I found {count} email address{'es' if count != 1 else ''}: {', '.join(data['emails'])}"
                else:
                    return "No email addresses were found in the provided text."

            elif "extract" in request_lower and "url" in request_lower:
                if "urls" in data and data["urls"]:
                    count = len(data["urls"])
                    return f"I found {count} URL{'s' if count != 1 else ''}: {', '.join(data['urls'])}"
                else:
                    return "No URLs were found in the provided text."

            # Generic fallback
            elif isinstance(data, dict) and data:
                key_results = []
                for key, value in list(data.items())[:3]:
                    if isinstance(value, list):
                        key_results.append(f"{key}: {len(value)} items")
                    elif isinstance(value, (int, float)):
                        key_results.append(f"{key}: {value}")

                if key_results:
                    return f"Results: {', '.join(key_results)}"

    return None


def extract_content_summary(agent_results):
    """Extract meaningful content from agent results."""
    content_parts = []

    for agent_name, agent_result in agent_results.items():
        if (
            not isinstance(agent_result, dict)
            or agent_result.get("status") != "success"
        ):
            continue

        agent_data = agent_result.get("data", {})

        # Email extraction
        if "email" in agent_name.lower() and isinstance(agent_data, dict):
            emails = agent_data.get("emails", [])
            if emails:
                content_parts.append(f"Found **{len(emails)} email addresses**:")
                for email in emails[:5]:  # Show first 5
                    content_parts.append(f"   • {email}")
                if len(emails) > 5:
                    content_parts.append(f"   • ... and {len(emails) - 5} more")

        # URL extraction
        elif "url" in agent_name.lower() and isinstance(agent_data, dict):
            urls = agent_data.get("urls", [])
            if urls:
                content_parts.append(f"Found **{len(urls)} URLs**:")
                for url in urls[:3]:  # Show first 3
                    content_parts.append(f"   • {url}")
                if len(urls) > 3:
                    content_parts.append(f"   • ... and {len(urls) - 3} more")

        # Generic data processing
        else:
            if isinstance(agent_data, dict) and agent_data:
                summary_items = []
                for key, value in list(agent_data.items())[:3]:
                    if isinstance(value, list):
                        summary_items.append(
                            f"**{key.replace('_', ' ').title()}**: {len(value)} items"
                        )
                    elif isinstance(value, (int, float)):
                        summary_items.append(
                            f"**{key.replace('_', ' ').title()}**: {value}"
                        )

                if summary_items:
                    content_parts.append(
                        f"**{agent_name.replace('_', ' ').title()} Results:**"
                    )
                    content_parts.extend([f"   • {item}" for item in summary_items])

    return content_parts


# Simple API endpoints
@api_bp.route("/workflow/<workflow_id>/status")
def get_workflow_status(workflow_id):
    """Get workflow status."""
    try:
        status = orchestrator_service.get_workflow_status(workflow_id)
        if not status:
            return jsonify({"error": "Workflow not found"}), 404
        return jsonify(status)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/registry/agents")
def list_agents():
    """Get list of available agents."""
    try:
        agents = registry_service.get_agents_list()
        return jsonify({"agents": agents, "count": len(agents)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/registry/tools")
def list_tools():
    """Get list of available tools."""
    try:
        tools = registry_service.get_tools_list()
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
            "messages": history,
        }

        response = make_response(json.dumps(export_data, indent=2))
        response.headers["Content-Type"] = "application/json"
        response.headers["Content-Disposition"] = (
            f'attachment; filename=chat_history_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        )
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Error handlers
@api_bp.errorhandler(400)
def bad_request(error):
    """Handle 400 errors."""
    return jsonify({"error": "Bad request"}), 400


@api_bp.errorhandler(404)
def not_found_api(error):
    """Handle 404 errors."""
    return jsonify({"error": "Endpoint not found"}), 404


@api_bp.errorhandler(500)
def internal_error_api(error):
    """Handle 500 errors."""
    return jsonify({"error": "Internal server error"}), 500


@api_bp.route("/workflows")
def list_workflows():
    """Get workflow history."""
    try:
        per_page = min(int(request.args.get("per_page", 20)), 100)
        workflows = orchestrator_service.get_workflow_history(limit=per_page)
        return jsonify(
            {"workflows": workflows, "count": len(workflows), "total": len(workflows)}
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/registry/dependencies")
def get_dependencies():
    """Get dependency graph."""
    try:
        deps = registry_service.get_dependency_graph()
        return jsonify(deps)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def get_current_workflow_status(self) -> Dict[str, Any]:
    """Get current workflow execution status for sidebar display."""
    try:
        # Get active workflows from orchestrator service
        from flask_app.services.orchestrator_service import orchestrator_service

        active_workflows = orchestrator_service.get_active_workflows()

        if not active_workflows:
            return {
                "status": "idle",
                "message": "No active workflows",
                "current_workflow": None,
            }

        # Get the most recent active workflow
        current = active_workflows[0]

        return {
            "status": "active",
            "message": f"Processing: {current.get('request', 'Unknown task')[:50]}...",
            "current_workflow": {
                "id": current.get("workflow_id"),
                "request": current.get("request"),
                "status": current.get("status"),
                "started_at": current.get("started_at"),
                "progress": self._calculate_workflow_progress(current),
            },
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error getting workflow status: {str(e)}",
            "current_workflow": None,
        }


@api_bp.route("/workflow/status/current")
def get_current_workflow_status():
    """Get current workflow status for sidebar display."""
    try:
        # Get active workflows from orchestrator service
        active_workflows = orchestrator_service.get_active_workflows()
        recent_workflows = orchestrator_service.get_workflow_history(limit=1)

        # If there's an active workflow, show it
        if active_workflows:
            current = active_workflows[0]
            return jsonify(
                {
                    "status": "active",
                    "message": f"Processing: {current.get('request', 'Unknown task')[:50]}...",
                    "current_workflow": {
                        "id": current.get("workflow_id"),
                        "request": current.get("request"),
                        "status": current.get("status"),
                        "started_at": current.get("started_at"),
                        "timeline": [],
                        "progress": (
                            50 if current.get("status") == "processing" else 100
                        ),
                    },
                    "workflow_results": {
                        "agentsUsed": len(current.get("agents", [])),
                        "executionTime": current.get("execution_time", 0),
                        "status": current.get("status", "Processing"),
                        "componentsCreated": 0,
                    },
                }
            )

        # If no active workflow, show the most recent completed one
        elif recent_workflows:
            recent = recent_workflows[0]
            return jsonify(
                {
                    "status": "completed",
                    "message": f"Last execution: {recent.get('request', 'Unknown task')[:50]}...",
                    "current_workflow": {
                        "id": recent.get("workflow_id"),
                        "request": recent.get("request"),
                        "status": "completed",
                        "started_at": recent.get("started_at"),
                        "timeline": [],
                        "progress": 100,
                    },
                    "workflow_results": {
                        "agentsUsed": recent.get(
                            "files", 0
                        ),  # This might need adjustment based on your data
                        "executionTime": recent.get("execution_time", 0),
                        "status": "Success",
                        "componentsCreated": 0,
                    },
                }
            )

        # No workflows at all
        else:
            return jsonify(
                {
                    "status": "idle",
                    "message": "No recent workflows",
                    "current_workflow": None,
                    "workflow_results": {
                        "agentsUsed": 0,
                        "executionTime": 0,
                        "status": "Idle",
                        "componentsCreated": 0,
                    },
                }
            )

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"Error getting workflow status: {str(e)}",
                    "current_workflow": None,
                    "workflow_results": {
                        "agentsUsed": 0,
                        "executionTime": 0,
                        "status": "Error",
                        "componentsCreated": 0,
                    },
                }
            ),
            500,
        )


@api_bp.route("/download/<filename>")
def download_file(filename):
    """Serve generated files for download."""
    try:
        # Security: Only allow downloading from outputs folder
        safe_filename = secure_filename(filename)
        file_path = os.path.join(current_app.config["OUTPUT_FOLDER"], safe_filename)

        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True, download_name=safe_filename)
        else:
            return jsonify({"error": "File not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/list-outputs")
def list_output_files():
    """List available output files for debugging."""
    try:
        output_dir = current_app.config["OUTPUT_FOLDER"]
        if os.path.exists(output_dir):
            files = [
                f
                for f in os.listdir(output_dir)
                if os.path.isfile(os.path.join(output_dir, f))
            ]
            return jsonify({"files": files, "output_dir": output_dir})
        else:
            return jsonify(
                {
                    "files": [],
                    "output_dir": output_dir,
                    "note": "Directory doesn't exist",
                }
            )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
