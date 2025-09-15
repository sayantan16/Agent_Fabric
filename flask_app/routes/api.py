# flask_app/routes/api.py - STREAMLINED VERSION
"""
API Routes Blueprint - Streamlined for Agentic Fabric POC
Handles AJAX requests, file uploads, and data endpoints
"""

import os
import json
from typing import Any, Dict, List
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
    """System health check endpoint - FIXED VERSION."""
    try:
        # FIXED: Use proper error handling for service availability checks
        health_status = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "services": {
                "orchestrator": {
                    "available": False,
                    "status": "unknown",
                    "message": "",
                },
                "registry": {"available": False, "status": "unknown", "message": ""},
                "workflow": {"available": False, "status": "unknown", "message": ""},
            },
            "system": {
                "uptime": "unknown",
                "memory_usage": "unknown",
                "active_workflows": 0,
            },
        }

        # Check orchestrator service
        try:
            orchestrator_available = orchestrator_service.is_backend_available()
            health_status["services"]["orchestrator"] = {
                "available": orchestrator_available,
                "status": "operational" if orchestrator_available else "degraded",
                "message": (
                    "Backend orchestrator ready"
                    if orchestrator_available
                    else "Backend orchestrator not available"
                ),
            }

            if orchestrator_available:
                health_status["system"]["active_workflows"] = len(
                    orchestrator_service.active_workflows
                )

        except Exception as e:
            health_status["services"]["orchestrator"] = {
                "available": False,
                "status": "error",
                "message": f"Orchestrator check failed: {str(e)}",
            }

        # Check registry service
        try:
            registry_available = registry_service.is_available()
            health_status["services"]["registry"] = {
                "available": registry_available,
                "status": "operational" if registry_available else "degraded",
                "message": (
                    "Registry service ready"
                    if registry_available
                    else "Registry service not available"
                ),
            }

            if registry_available:
                health_status["registry_stats"] = registry_service.get_registry_stats()

        except Exception as e:
            health_status["services"]["registry"] = {
                "available": False,
                "status": "error",
                "message": f"Registry check failed: {str(e)}",
            }

        # Check workflow service
        try:
            workflow_available = workflow_service.is_available()
            health_status["services"]["workflow"] = {
                "available": workflow_available,
                "status": "operational" if workflow_available else "degraded",
                "message": (
                    "Workflow engine ready"
                    if workflow_available
                    else "Workflow engine not available"
                ),
            }
        except Exception as e:
            health_status["services"]["workflow"] = {
                "available": False,
                "status": "error",
                "message": f"Workflow check failed: {str(e)}",
            }

        # Determine overall system status
        services_available = sum(
            1 for s in health_status["services"].values() if s["available"]
        )
        total_services = len(health_status["services"])

        if services_available == total_services:
            health_status["status"] = "healthy"
        elif services_available > 0:
            health_status["status"] = "degraded"
        else:
            health_status["status"] = "unhealthy"

        # Add system information
        try:
            import psutil
            import time

            health_status["system"][
                "uptime"
            ] = f"{time.time() - psutil.boot_time():.1f}s"
            health_status["system"][
                "memory_usage"
            ] = f"{psutil.virtual_memory().percent}%"
        except ImportError:
            # psutil not available, use defaults
            pass

        return jsonify(health_status)

    except Exception as e:
        # FIXED: Always return a valid response even on complete failure
        return (
            jsonify(
                {
                    "status": "error",
                    "timestamp": datetime.now().isoformat(),
                    "error": f"Health check failed: {str(e)}",
                    "services": {
                        "orchestrator": {
                            "available": False,
                            "status": "error",
                            "message": "Health check failed",
                        },
                        "registry": {
                            "available": False,
                            "status": "error",
                            "message": "Health check failed",
                        },
                        "workflow": {
                            "available": False,
                            "status": "error",
                            "message": "Health check failed",
                        },
                    },
                }
            ),
            500000,
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

        # NEW: Add pipeline detection and routing
        import asyncio

        try:
            # Simple complexity detection
            request_lower = message.lower()
            pipeline_keywords = [
                "then",
                "after",
                "and",
                "extract and",
                "analyze and",
                "step",
                "first",
                "next",
            ]
            is_complex = (
                any(keyword in request_lower for keyword in pipeline_keywords)
                or len(files) > 1
            )

            if is_complex:
                # Use pipeline processing (if you implement process_pipeline_request)
                # For now, use regular processing but mark as pipeline
                result = asyncio.run(
                    orchestrator_service.process_user_request(
                        request_text=message,
                        files=files,
                        auto_create=auto_create,
                    )
                )
                # Mark as pipeline result
                result.setdefault("metadata", {})["is_pipeline"] = True
            else:
                # Use regular processing
                result = asyncio.run(
                    orchestrator_service.process_user_request(
                        request_text=message,
                        files=files,
                        auto_create=auto_create,
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

        # Add system response to session with pipeline info
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
                # NEW: Add pipeline info
                "pipeline_info": {
                    "type": (
                        "pipeline"
                        if len(result.get("workflow", {}).get("steps", [])) > 1
                        else "simple"
                    ),
                    "steps": result.get("workflow", {}).get("steps", []),
                    "steps_completed": len(result.get("workflow", {}).get("steps", [])),
                    "total_steps": len(result.get("workflow", {}).get("steps", [])),
                    "execution_time": result.get("execution_time", 0),
                    "performance_grade": (
                        "excellent"
                        if result.get("status") == "success"
                        else "acceptable"
                    ),
                    "components_created": result.get("metadata", {}).get(
                        "components_created", 0
                    ),
                },
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
                # NEW: Add pipeline-specific data for frontend
                "pipeline_info": system_response["metadata"]["pipeline_info"],
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
    """Get current workflow status - FIXED VERSION."""
    try:
        # FIXED: Handle case where orchestrator_service might not be fully initialized
        if not hasattr(orchestrator_service, "active_workflows"):
            return jsonify(
                {
                    "status": "no_active_workflows",
                    "active_workflows": {},
                    "message": "Orchestrator service not fully initialized",
                }
            )

        active_workflows = orchestrator_service.active_workflows

        if not active_workflows:
            return jsonify(
                {
                    "status": "no_active_workflows",
                    "active_workflows": {},
                    "message": "No workflows currently running",
                }
            )

        return jsonify(
            {
                "status": "success",
                "active_workflows": active_workflows,
                "count": len(active_workflows),
            }
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "error": f"Failed to get workflow status: {str(e)}",
                    "active_workflows": {},
                }
            ),
            500000,
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


@api_bp.route("/chat/pipeline", methods=["POST"])
async def process_pipeline_chat():
    """Enhanced chat endpoint with pipeline support."""
    try:
        data = request.get_json()

        if not data or "message" not in data:
            return jsonify({"error": "Message is required"}), 400

        user_message = data["message"].strip()
        if not user_message:
            return jsonify({"error": "Message cannot be empty"}), 400

        auto_create = data.get("auto_create", True)
        session_id = session.get("session_id", str(uuid.uuid4()))
        session["session_id"] = session_id

        # Get uploaded files from session
        uploaded_files = session.get("uploaded_files", [])

        print(f"DEBUG: Processing pipeline chat - Message: {user_message[:100]}...")

        # Process through enhanced pipeline orchestrator
        result = await orchestrator_service.process_pipeline_request(
            request_text=user_message, files=uploaded_files, auto_create=auto_create
        )

        # Create chat message entry
        chat_entry = {
            "id": str(uuid.uuid4()),
            "type": "user",
            "content": user_message,
            "timestamp": datetime.now().isoformat(),
            "files": len(uploaded_files),
            "workflow_id": result.get("workflow_id"),
        }

        # Create response entry
        response_entry = {
            "id": str(uuid.uuid4()),
            "type": "assistant",
            "content": result.get(
                "response", "I encountered an issue processing your request."
            ),
            "timestamp": datetime.now().isoformat(),
            "workflow": result.get("workflow", {}),
            "status": result.get("status", "unknown"),
            "metadata": result.get("metadata", {}),
            "pipeline_info": {
                "type": result.get("workflow", {}).get("type", "unknown"),
                "steps_completed": result.get("workflow", {}).get("steps_completed", 0),
                "total_steps": result.get("workflow", {}).get("total_steps", 0),
                "execution_time": result.get("metadata", {}).get("execution_time", 0),
                "performance_grade": result.get("metadata", {}).get(
                    "performance_grade", "unknown"
                ),
            },
        }

        # Add to chat history
        if "chat_history" not in session:
            session["chat_history"] = []

        session["chat_history"].extend([chat_entry, response_entry])
        session.modified = True

        # Clear uploaded files after processing
        session["uploaded_files"] = []

        return jsonify(
            {
                "response": response_entry,
                "workflow": result.get("workflow", {}),
                "status": result.get("status"),
                "pipeline_info": response_entry["pipeline_info"],
                "generated_files": result.get("generated_files", []),
                "errors": result.get("errors", []),
            }
        )

    except Exception as e:
        current_app.logger.error(f"Pipeline chat error: {str(e)}")
        return (
            jsonify(
                {
                    "error": "An error occurred processing your request",
                    "details": str(e) if current_app.debug else None,
                }
            ),
            500,
        )


@api_bp.route("/pipeline/analytics")
def get_pipeline_analytics():
    """Get pipeline processing analytics."""
    try:
        analytics = orchestrator_service.get_pipeline_analytics()
        return jsonify(analytics)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/components/pipeline")
def get_pipeline_components():
    """Get information about pipeline-capable components."""
    try:
        # Get all agents and filter for pipeline-capable ones
        all_agents = registry_service.get_agents_list()
        pipeline_agents = [
            agent
            for agent in all_agents
            if "pipeline" in agent.get("tags", [])
            or agent.get("metadata", {}).get("created_for_pipeline", False)
        ]

        # Get tools that support pipeline operations
        all_tools = registry_service.get_tools_list()
        pipeline_tools = [
            tool
            for tool in all_tools
            if any(
                keyword in tool.get("description", "").lower()
                for keyword in ["format", "convert", "adapt", "process"]
            )
        ]

        return jsonify(
            {
                "pipeline_agents": {
                    "count": len(pipeline_agents),
                    "agents": pipeline_agents,
                },
                "pipeline_tools": {
                    "count": len(pipeline_tools),
                    "tools": pipeline_tools,
                },
                "total_components": len(pipeline_agents) + len(pipeline_tools),
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/workflows/pipeline")
def list_pipeline_workflows():
    """Get list of pipeline workflows."""
    try:
        # Get pipeline workflows from history
        pipeline_workflows = [
            w
            for w in orchestrator_service.workflow_history
            if w.get("type") == "pipeline"
        ]

        # Sort by most recent first
        pipeline_workflows.sort(key=lambda x: x.get("started_at", ""), reverse=True)

        return jsonify(
            {
                "workflows": pipeline_workflows,
                "count": len(pipeline_workflows),
                "analytics": orchestrator_service.get_pipeline_analytics(),
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500
