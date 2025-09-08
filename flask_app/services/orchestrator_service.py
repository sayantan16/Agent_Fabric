# flask_app/services/orchestrator_service.py
"""
Orchestrator Service
Interfaces with core/orchestrator.py for request processing
"""

import os
import sys
import asyncio
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

# Add project root to path for backend imports
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(project_root)

try:
    from core.orchestrator import Orchestrator
    from core.registry_singleton import get_shared_registry
except ImportError as e:
    print(f"Warning: Could not import backend components: {e}")
    Orchestrator = None


class OrchestratorService:
    """Service layer for orchestrator operations."""

    def __init__(self):
        """Initialize orchestrator service."""
        try:
            self.orchestrator = Orchestrator() if Orchestrator else None
        except Exception as e:
            print(f"Warning: Could not initialize Orchestrator: {e}")
            self.orchestrator = None
        self.active_workflows = {}
        self.workflow_history = []

        # Add sample data for demonstration
        self.create_sample_workflows()

    def is_backend_available(self) -> bool:
        """Check if backend components are available."""
        return self.orchestrator is not None

    async def process_user_request(
        self,
        request_text: str,
        files: List[Dict] = None,
        auto_create: bool = True,
        workflow_type: str = "sequential",
    ) -> Dict[str, Any]:
        """
        Process user request through orchestrator.

        Args:
            request_text: User's natural language request
            files: List of uploaded files with metadata
            auto_create: Whether to auto-create missing agents
            workflow_type: Type of workflow execution

        Returns:
            Processed result with workflow information
        """
        workflow_id = f"wf_{uuid.uuid4().hex[:8]}"

        try:
            if not self.is_backend_available():
                return {
                    "status": "error",
                    "workflow_id": workflow_id,
                    "error": "Backend orchestrator not available",
                    "message": "Please check backend configuration",
                }

            # Prepare request data
            request_data = {
                "request": request_text,
                "files": files or [],
                "workflow_id": workflow_id,
                "workflow_type": workflow_type,
                "auto_create": auto_create,
                "started_at": datetime.now().isoformat(),
            }

            # Track workflow start
            self.active_workflows[workflow_id] = {
                "status": "processing",
                "started_at": request_data["started_at"],
                "request": request_text,
                "files": len(files) if files else 0,
            }

            # Process through orchestrator
            result = await self.orchestrator.process_request(
                user_request=request_text, files=files, auto_create=auto_create
            )

            # Update workflow status
            final_status = result.get("status", "unknown")
            self.active_workflows[workflow_id]["status"] = final_status
            self.active_workflows[workflow_id][
                "completed_at"
            ] = datetime.now().isoformat()

            # Add workflow metadata
            result["workflow_id"] = workflow_id
            result["request_data"] = request_data

            # Move to history if completed
            if final_status in ["success", "error", "partial"]:
                self.workflow_history.append(self.active_workflows[workflow_id])
                if workflow_id in self.active_workflows:
                    del self.active_workflows[workflow_id]

            return result

        except Exception as e:
            # Handle processing errors
            error_result = {
                "status": "error",
                "workflow_id": workflow_id,
                "error": str(e),
                "message": "Request processing failed",
                "request_data": locals().get("request_data", {}),
                "traceback": str(e),
            }

            # Update workflow status
            if workflow_id in self.active_workflows:
                self.active_workflows[workflow_id]["status"] = "error"
                self.active_workflows[workflow_id]["error"] = str(e)

            return error_result

    def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get current status of a workflow."""

        # Check active workflows
        if workflow_id in self.active_workflows:
            return self.active_workflows[workflow_id]

        # Check history
        for workflow in self.workflow_history:
            if workflow.get("workflow_id") == workflow_id:
                return workflow

        return None

    def cancel_workflow(self, workflow_id: str) -> bool:
        """Cancel an active workflow."""
        if workflow_id in self.active_workflows:
            self.active_workflows[workflow_id]["status"] = "cancelled"
            self.active_workflows[workflow_id][
                "cancelled_at"
            ] = datetime.now().isoformat()
            return True
        return False

    def get_active_workflows(self) -> List[Dict[str, Any]]:
        """Get list of currently active workflows."""
        active = list(self.active_workflows.values())

        # Ensure each active workflow has required fields
        for workflow in active:
            workflow.setdefault(
                "workflow_id", workflow.get("id", f"active_{len(active)}")
            )
            workflow.setdefault("request", "Active workflow processing...")
            workflow.setdefault("status", "processing")
            workflow.setdefault("started_at", datetime.now().isoformat())

        return active

    def get_workflow_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent workflow history."""
        history = self.workflow_history[-limit:] if self.workflow_history else []

        # Ensure each workflow has required fields for the template
        for workflow in history:
            workflow.setdefault("workflow_id", f"wf_{len(history)}")
            workflow.setdefault("request", "Sample workflow request")
            workflow.setdefault("status", "completed")
            workflow.setdefault("started_at", datetime.now().isoformat())
            workflow.setdefault("execution_time", 2.5)
            workflow.setdefault("files", 0)

        return history

    def get_system_stats(self) -> Dict[str, Any]:
        """Get system performance statistics."""
        return {
            "active_workflows": len(self.active_workflows),
            "total_processed": len(self.workflow_history),
            "backend_available": self.is_backend_available(),
            "avg_processing_time": self._calculate_avg_processing_time(),
            "success_rate": self._calculate_success_rate(),
        }

    def _calculate_avg_processing_time(self) -> float:
        """Calculate average processing time from history."""
        if not self.workflow_history:
            return 0.0

        total_time = 0
        count = 0

        for workflow in self.workflow_history:
            if "started_at" in workflow and "completed_at" in workflow:
                try:
                    start = datetime.fromisoformat(workflow["started_at"])
                    end = datetime.fromisoformat(workflow["completed_at"])
                    total_time += (end - start).total_seconds()
                    count += 1
                except:
                    continue

        return total_time / count if count > 0 else 0.0

    def _calculate_success_rate(self) -> float:
        """Calculate success rate from history."""
        if not self.workflow_history:
            return 1.0

        successful = sum(
            1 for w in self.workflow_history if w.get("status") == "success"
        )
        return successful / len(self.workflow_history)

    def create_sample_workflows(self):
        """Create sample workflow data for demonstration."""
        if not self.workflow_history:  # Only create if empty
            sample_workflows = [
                {
                    "workflow_id": "wf_demo_001",
                    "request": "Extract emails from uploaded document",
                    "status": "success",
                    "started_at": (datetime.now() - timedelta(hours=2)).isoformat(),
                    "completed_at": (
                        datetime.now() - timedelta(hours=2) + timedelta(minutes=5)
                    ).isoformat(),
                    "execution_time": 4.2,
                    "files": 1,
                },
                {
                    "workflow_id": "wf_demo_002",
                    "request": "Analyze CSV data and create statistical report",
                    "status": "success",
                    "started_at": (datetime.now() - timedelta(hours=1)).isoformat(),
                    "completed_at": (
                        datetime.now() - timedelta(hours=1) + timedelta(minutes=8)
                    ).isoformat(),
                    "execution_time": 7.8,
                    "files": 1,
                },
                {
                    "workflow_id": "wf_demo_003",
                    "request": "Extract phone numbers and URLs from text",
                    "status": "partial",
                    "started_at": (datetime.now() - timedelta(minutes=30)).isoformat(),
                    "completed_at": (
                        datetime.now() - timedelta(minutes=25)
                    ).isoformat(),
                    "execution_time": 3.1,
                    "files": 0,
                },
            ]
            self.workflow_history.extend(sample_workflows)


# Global service instance
orchestrator_service = OrchestratorService()
