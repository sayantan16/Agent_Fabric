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
    """Create a natural language response from orchestrator results."""

    # Check if we have a synthesized response from orchestrator
    if result.get("response"):
        # Use the orchestrator's synthesized response
        return result["response"]

    # Fallback: Create response from components
    if result.get("status") == "error":
        error_msg = result.get("error", "An unknown error occurred")
        return f"I encountered an error while processing your request: {error_msg}\n\nPlease try again or provide more specific information."

    # Build response from results
    response_parts = []

    # Add opening based on request type
    if "extract" in original_request.lower():
        response_parts.append(
            "I've extracted the requested information from your content:"
        )
    elif "analyze" in original_request.lower():
        response_parts.append("I've completed the analysis of your content:")
    else:
        response_parts.append("I've processed your request successfully:")

    # Process agent results
    agent_results = result.get("results", {})
    workflow_steps = result.get("workflow", {}).get("steps", [])

    # Extract meaningful content from each agent
    all_emails = []
    all_urls = []
    all_phones = []
    other_data = {}

    for agent_name, agent_result in agent_results.items():
        if (
            not isinstance(agent_result, dict)
            or agent_result.get("status") != "success"
        ):
            continue

        agent_data = agent_result.get("data", {})

        # Collect specific data types
        if isinstance(agent_data, dict):
            if "emails" in agent_data:
                all_emails.extend(agent_data["emails"])
            if "urls" in agent_data:
                all_urls.extend(agent_data["urls"])
            if "phones" in agent_data:
                all_phones.extend(agent_data["phones"])

            # Collect other data
            for key, value in agent_data.items():
                if key not in ["emails", "urls", "phones"]:
                    other_data[key] = value

    # Format findings
    if all_emails:
        response_parts.append(f"\n📧 **Email Addresses Found ({len(all_emails)}):**")
        for email in all_emails[:10]:  # Limit display
            response_parts.append(f"  • {email}")
        if len(all_emails) > 10:
            response_parts.append(f"  • ... and {len(all_emails) - 10} more")

    if all_urls:
        response_parts.append(f"\n🔗 **URLs Found ({len(all_urls)}):**")
        for url in all_urls[:10]:
            response_parts.append(f"  • {url}")
        if len(all_urls) > 10:
            response_parts.append(f"  • ... and {len(all_urls) - 10} more")

    if all_phones:
        response_parts.append(f"\n📞 **Phone Numbers Found ({len(all_phones)}):**")
        for phone in all_phones[:10]:
            response_parts.append(f"  • {phone}")

    # Add other data if present
    if other_data:
        response_parts.append("\n📊 **Additional Information:**")
        for key, value in list(other_data.items())[:5]:
            response_parts.append(f"  • {key.replace('_', ' ').title()}: {value}")

    # If no specific data found
    if not (all_emails or all_urls or all_phones or other_data):
        response_parts.append(
            "\nNo specific data items were extracted from your content."
        )

    # Add execution summary
    if workflow_steps:
        response_parts.append(f"\n---")
        response_parts.append(
            f"*Processed using {len(workflow_steps)} agents in {result.get('execution_time', 0):.1f} seconds*"
        )

    return "\n".join(response_parts)


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


def _calculate_workflow_progress(self, workflow_data: Dict) -> int:
    """Calculate workflow progress percentage."""
    # This is a simple calculation - you can make it more sophisticated
    if workflow_data.get("status") == "completed":
        return 100
    elif workflow_data.get("status") == "processing":
        return 50  # Assume 50% when processing
    else:
        return 0


# @api_bp.route("/workflow/status/current")
# def get_current_workflow_status():
#     """Get current workflow status for sidebar display."""
#     try:
#         # Get active workflows from orchestrator service
#         active_workflows = orchestrator_service.get_active_workflows()
#         recent_workflows = orchestrator_service.get_workflow_history(limit=1)

#         # If there's an active workflow, show it
#         if active_workflows:
#             current = active_workflows[0]
#             return jsonify(
#                 {
#                     "status": "active",
#                     "message": f"Processing: {current.get('request', 'Unknown task')[:50]}...",
#                     "current_workflow": {
#                         "id": current.get("workflow_id"),
#                         "request": current.get("request"),
#                         "status": current.get("status"),
#                         "started_at": current.get("started_at"),
#                         "timeline": [],
#                         "progress": (
#                             50 if current.get("status") == "processing" else 100
#                         ),
#                     },
#                     "workflow_results": {
#                         "agentsUsed": len(current.get("agents", [])),
#                         "executionTime": current.get("execution_time", 0),
#                         "status": current.get("status", "Processing"),
#                         "componentsCreated": 0,
#                     },
#                 }
#             )

#         # If no active workflow, show the most recent completed one
#         elif recent_workflows:
#             recent = recent_workflows[0]
#             return jsonify(
#                 {
#                     "status": "completed",
#                     "message": f"Last execution: {recent.get('request', 'Unknown task')[:50]}...",
#                     "current_workflow": {
#                         "id": recent.get("workflow_id"),
#                         "request": recent.get("request"),
#                         "status": "completed",
#                         "started_at": recent.get("started_at"),
#                         "timeline": [],
#                         "progress": 100,
#                     },
#                     "workflow_results": {
#                         "agentsUsed": recent.get(
#                             "files", 0
#                         ),  # This might need adjustment based on your data
#                         "executionTime": recent.get("execution_time", 0),
#                         "status": "Success",
#                         "componentsCreated": 0,
#                     },
#                 }
#             )

#         # No workflows at all
#         else:
#             return jsonify(
#                 {
#                     "status": "idle",
#                     "message": "No recent workflows",
#                     "current_workflow": None,
#                     "workflow_results": {
#                         "agentsUsed": 0,
#                         "executionTime": 0,
#                         "status": "Idle",
#                         "componentsCreated": 0,
#                     },
#                 }
#             )

#     except Exception as e:
#         return (
#             jsonify(
#                 {
#                     "status": "error",
#                     "message": f"Error getting workflow status: {str(e)}",
#                     "current_workflow": None,
#                     "workflow_results": {
#                         "agentsUsed": 0,
#                         "executionTime": 0,
#                         "status": "Error",
#                         "componentsCreated": 0,
#                     },
#                 }
#             ),
#             500,
#         )
