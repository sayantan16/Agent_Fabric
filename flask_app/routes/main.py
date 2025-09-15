# flask_app/routes/main.py
"""
Main Routes Blueprint
Handles page rendering and navigation
"""

from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from flask_app.services.registry_service import registry_service
from flask_app.services.orchestrator_service import orchestrator_service
import os

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Main chat interface page with enhanced system status."""
    try:
        # Get chat history from session
        chat_history = session.get("chat_history", [])
        # Get comprehensive system status with safe defaults
        system_status = {
            "backend_available": registry_service.is_available(),
            "registry_stats": registry_service.get_registry_stats() or {},
            "recent_workflows": [],  # Start with empty list
            "system_performance": {},  # Start with empty dict
        }

        # Only try to get workflows if orchestrator is available
        try:
            if orchestrator_service.is_backend_available():
                system_status["recent_workflows"] = (
                    orchestrator_service.get_workflow_history(limit=5) or []
                )
                system_status["system_performance"] = (
                    orchestrator_service.get_system_stats() or {}
                )
        except Exception as e:
            print(f"Warning: Could not get orchestrator data: {e}")
            # Continue with empty data rather than failing

        # Get session-based chat history with safe default
        chat_history = session.get("chat_history", [])

        # Get user preferences with safe defaults
        user_settings = {
            "auto_create": session.get("auto_create", True),
            "workflow_type": session.get("workflow_type", "sequential"),
            "theme": session.get("theme", "light"),
            "show_debug": session.get("debug_mode", False),
        }

        return render_template(
            "index.jinja2",  # Use correct template name
            system_status=system_status,
            chat_history=chat_history,
            user_settings=user_settings,
        )

    except Exception as e:
        print(f"Error in index route: {str(e)}")
        import traceback

        traceback.print_exc()
        flash(f"Error loading chat interface: {str(e)}", "error")
        return render_template(
            "error.html", error_code=500, error_message="Failed to load chat interface"
        )


@main_bp.route("/registry")
def registry():
    """Registry explorer page."""
    try:
        # Get filter parameters
        agent_tags = request.args.getlist("agent_tags")
        tool_tags = request.args.getlist("tool_tags")
        search_query = request.args.get("search", "").strip()

        # Fetch data with safe defaults
        agents = (
            registry_service.get_agents_list(tags=agent_tags if agent_tags else None)
            or []
        )

        tools = (
            registry_service.get_tools_list(tags=tool_tags if tool_tags else None) or []
        )

        registry_stats = registry_service.get_registry_stats() or {
            "available": False,
            "statistics": {"total_agents": 0, "total_tools": 0},
            "summary": {"health_score": 0, "status": "unavailable"},
        }

        # Apply search filter if provided
        if search_query:
            search_results = registry_service.search_components(search_query)
            agents = search_results.get("agents", [])
            tools = search_results.get("tools", [])

        # Get all available tags for filters
        all_agent_tags = set()
        all_tool_tags = set()

        for agent in registry_service.get_agents_list() or []:
            all_agent_tags.update(agent.get("tags", []))

        for tool in registry_service.get_tools_list() or []:
            all_tool_tags.update(tool.get("tags", []))

        return render_template(
            "registry.html",
            agents=agents,
            tools=tools,
            registry_stats=registry_stats,
            all_agent_tags=sorted(all_agent_tags),
            all_tool_tags=sorted(all_tool_tags),
            current_filters={
                "agent_tags": agent_tags,
                "tool_tags": tool_tags,
                "search": search_query,
            },
        )

    except Exception as e:
        print(f"Registry error: {str(e)}")
        import traceback

        traceback.print_exc()
        flash(f"Error loading registry: {str(e)}", "error")
        return render_template(
            "error.html", error_code=500, error_message="Failed to load registry"
        )


@main_bp.route("/workflows")
def workflows():
    """Workflow history and management page."""
    try:
        # Get real workflow history from orchestrator service
        all_workflows = []
        active_workflows = []

        try:
            all_workflows = orchestrator_service.get_workflow_history() or []
            active_workflows = orchestrator_service.get_active_workflows() or []
        except Exception as e:
            print(f"Error getting workflow data: {e}")
            # Fallback to empty lists

        # Get pagination parameters
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 20))

        # Apply pagination
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        workflows = all_workflows[start_idx:end_idx]

        pagination_info = {
            "page": page,
            "per_page": per_page,
            "total": len(all_workflows),
            "pages": max(1, (len(all_workflows) + per_page - 1) // per_page),
            "has_prev": page > 1,
            "has_next": end_idx < len(all_workflows),
        }

        # Get system stats
        system_stats = {
            "avg_processing_time": sum(
                w.get("execution_time", 0) for w in all_workflows
            )
            / max(len(all_workflows), 1),
            "success_rate": len(
                [w for w in all_workflows if w.get("status") == "success"]
            )
            / max(len(all_workflows), 1),
            "total_processed": len(all_workflows),
            "active_workflows": len(active_workflows),
        }

        return render_template(
            "workflows.html",
            workflows=workflows,
            active_workflows=active_workflows,
            pagination=pagination_info,
            system_stats=system_stats,
        )

    except Exception as e:
        print(f"Workflows error: {str(e)}")
        flash(f"Error loading workflows: {str(e)}", "error")
        return render_template(
            "error.html", error_code=500, error_message="Failed to load workflows"
        )


@main_bp.route("/workflow/<workflow_id>")
def workflow_detail(workflow_id):
    """Detailed view of a specific workflow."""
    try:
        # Get workflow status and details
        workflow_status = orchestrator_service.get_workflow_status(workflow_id)

        if not workflow_status:
            flash("Workflow not found", "error")
            return redirect(url_for("main.workflows"))

        # Get visualization data
        from flask_app.services import workflow_service

        viz_data = workflow_service.get_workflow_visualization(workflow_id)

        return render_template(
            "workflow_detail.jinja2",
            workflow=workflow_status,
            visualization=viz_data,
            workflow_id=workflow_id,
        )

    except Exception as e:
        flash(f"Error loading workflow details: {str(e)}", "error")
        return redirect(url_for("main.workflows"))


@main_bp.route("/agent/<agent_name>")
def agent_detail(agent_name):
    """Detailed view of a specific agent."""
    try:
        agent = registry_service.get_agent_details(agent_name)

        if not agent:
            flash("Agent not found", "error")
            return redirect(url_for("main.registry"))

        return render_template("agent_detail.html", agent=agent, agent_name=agent_name)

    except Exception as e:
        flash(f"Error loading agent details: {str(e)}", "error")
        return redirect(url_for("main.registry"))


@main_bp.route("/tool/<tool_name>")
def tool_detail(tool_name):
    """Detailed view of a specific tool."""
    try:
        tool = registry_service.get_tool_details(tool_name)

        if not tool:
            flash("Tool not found", "error")
            return redirect(url_for("main.registry"))

        return render_template("tool_detail.html", tool=tool, tool_name=tool_name)

    except Exception as e:
        flash(f"Error loading tool details: {str(e)}", "error")
        return redirect(url_for("main.registry"))


# Error handlers for this blueprint
@main_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors within main blueprint."""
    return (
        render_template("error.html", error_code=404, error_message="Page not found"),
        404,
    )


@main_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors within main blueprint."""
    return (
        render_template(
            "error.html", error_code=500, error_message="Internal server error"
        ),
        500,
    )
