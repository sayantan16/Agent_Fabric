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

from core.pipeline_orchestrator import PipelineOrchestrator
from core.workflow_intelligence import WorkflowIntelligence


# Add project root to path for backend imports
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(project_root)

try:
    from core.simplified_orchestrator import Orchestrator
    from core.registry_singleton import get_shared_registry
    from core.pipeline_orchestrator import PipelineOrchestrator
    from core.workflow_intelligence import WorkflowIntelligence
except ImportError as e:
    print(f"Warning: Could not import backend components: {e}")
    Orchestrator = None
    PipelineOrchestrator = None
    WorkflowIntelligence = None


class OrchestratorService:
    """Service layer for orchestrator operations."""

    def __init__(self):
        """Initialize orchestrator service with pipeline support - FIXED VERSION."""
        # FIXED: Initialize all attributes first to prevent AttributeError
        self.orchestrator = None
        self.registry = None
        self.pipeline_orchestrator = None
        self.workflow_intelligence = None
        self.active_workflows = {}
        self.workflow_history = []  # FIXED: Always initialize this attribute

        try:
            # Try to initialize backend components
            if Orchestrator:
                self.orchestrator = Orchestrator()
                print("DEBUG: Orchestrator initialized successfully")

            # Get shared registry
            if get_shared_registry:
                self.registry = get_shared_registry()
                print("DEBUG: Registry obtained successfully")

            # Initialize pipeline components if available
            if PipelineOrchestrator:
                self.pipeline_orchestrator = PipelineOrchestrator()
                print("DEBUG: PipelineOrchestrator initialized successfully")

            if WorkflowIntelligence and self.registry:
                self.workflow_intelligence = WorkflowIntelligence(self.registry)
                print("DEBUG: WorkflowIntelligence initialized successfully")

            print("DEBUG: OrchestratorService initialized with all components")

        except Exception as e:
            print(f"WARNING: Failed to initialize some orchestrator components: {e}")
            # Ensure all attributes are still set even if initialization fails

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
                    "results": {},
                    "execution_time": 0,
                    "metadata": {
                        "agents_used": [],
                        "workflow_type": workflow_type,
                        "execution_time": 0,
                        "components_created": 0,
                        "pipeline_info": {
                            "type": "simple",
                            "steps": [],
                            "steps_completed": 0,
                            "total_steps": 0,
                            "execution_time": 0,
                            "components_created": 0,
                            "performance_grade": "acceptable",
                        },
                    },
                    "pipeline_info": {
                        "type": "simple",
                        "steps": [],
                        "steps_completed": 0,
                        "total_steps": 0,
                        "execution_time": 0,
                        "components_created": 0,
                        "performance_grade": "acceptable",
                    },
                    "workflow": {},
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

            # Store workflow as active
            self.active_workflows[workflow_id] = {
                "status": "processing",
                "request": request_text,
                "started_at": datetime.now().isoformat(),
                "workflow_type": workflow_type,
            }

            # Process through orchestrator
            start_time = datetime.now()
            result = await self.orchestrator.process_request(
                user_request=request_text,
                files=files,
                auto_create=auto_create,
            )
            execution_time = (datetime.now() - start_time).total_seconds()

            # Update workflow status
            workflow_data = {
                "workflow_id": workflow_id,
                "request": request_text,
                "status": result.get("status", "completed"),
                "started_at": request_data["started_at"],
                "completed_at": datetime.now().isoformat(),
                "execution_time": execution_time,
                "workflow_type": workflow_type,
                "files": len(files) if files else 0,
                "agents_used": result.get("agents_used", []),
                "results": result.get("results", {}),
            }

            # Add to history
            self.workflow_history.append(workflow_data)

            # Remove from active workflows
            if workflow_id in self.active_workflows:
                del self.active_workflows[workflow_id]

            # Format response for UI
            return {
                "status": "success",
                "workflow_id": workflow_id,
                "response": result.get("response", "Request processed successfully"),
                "results": result.get("results", {}),
                "execution_time": execution_time,
                "metadata": {
                    "agents_used": result.get("agents_used", []),
                    "workflow_type": workflow_type,
                    "execution_time": execution_time,
                    "components_created": result.get("components_created", 0),
                    "pipeline_info": {
                        "type": "simple",
                        "steps": result.get("pipeline_steps", []),
                        "steps_completed": len(result.get("pipeline_steps", [])),
                        "total_steps": len(result.get("pipeline_steps", [])),
                        "execution_time": execution_time,
                        "components_created": result.get("components_created", 0),
                        "performance_grade": (
                            "good" if execution_time < 10 else "acceptable"
                        ),
                    },
                },
                "pipeline_info": {
                    "type": "simple",
                    "steps": result.get("pipeline_steps", []),
                    "steps_completed": len(result.get("pipeline_steps", [])),
                    "total_steps": len(result.get("pipeline_steps", [])),
                    "execution_time": execution_time,
                    "components_created": result.get("components_created", 0),
                    "performance_grade": (
                        "good" if execution_time < 10 else "acceptable"
                    ),
                },
                "workflow": workflow_data,
                "chat_updated": True,
                "message_id": f"msg_{uuid.uuid4().hex[:8]}",
            }

        except Exception as e:
            print(f"ERROR: Failed to process request: {e}")

            # Ensure workflow is removed from active and added to history even on error
            if workflow_id in self.active_workflows:
                del self.active_workflows[workflow_id]

            error_workflow = {
                "workflow_id": workflow_id,
                "request": request_text,
                "status": "error",
                "started_at": datetime.now().isoformat(),
                "completed_at": datetime.now().isoformat(),
                "execution_time": 0,
                "error": str(e),
            }
            self.workflow_history.append(error_workflow)

            return {
                "status": "error",
                "workflow_id": workflow_id,
                "error": f"Failed to process request: {str(e)}",
                "message": "An error occurred while processing your request",
                "results": {},
                "execution_time": 0,
                "metadata": {
                    "agents_used": [],
                    "workflow_type": workflow_type,
                    "execution_time": 0,
                    "components_created": 0,
                    "pipeline_info": {
                        "type": "simple",
                        "steps": [],
                        "steps_completed": 0,
                        "total_steps": 0,
                        "execution_time": 0,
                        "components_created": 0,
                        "performance_grade": "poor",
                    },
                },
                "pipeline_info": {
                    "type": "simple",
                    "steps": [],
                    "steps_completed": 0,
                    "total_steps": 0,
                    "execution_time": 0,
                    "components_created": 0,
                    "performance_grade": "poor",
                },
                "workflow": error_workflow,
                "chat_updated": True,
                "message_id": f"msg_{uuid.uuid4().hex[:8]}",
            }

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

    def get_workflow_metrics(self) -> Dict[str, Any]:
        """Get workflow performance metrics."""
        if not self.workflow_history:
            return {"total": 0, "success_rate": 0, "avg_execution_time": 0}

        total = len(self.workflow_history)
        successful = len(
            [w for w in self.workflow_history if w.get("status") == "success"]
        )
        avg_time = (
            sum(w.get("execution_time", 0) for w in self.workflow_history) / total
        )

        return {
            "total": total,
            "success_rate": successful / total,
            "avg_execution_time": avg_time,
            "active_workflows": len(self.active_workflows),
        }

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
                    "agents_used": ["email_extractor"],
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
                    "agents_used": ["read_csv", "word_counter"],
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
                    "agents_used": ["url_extractor"],
                },
            ]
            self.workflow_history.extend(sample_workflows)
            print("DEBUG: Sample workflows created")

    def get_pipeline_analytics(self) -> Dict[str, Any]:
        """Get pipeline performance analytics."""
        # Get last 10 pipeline workflows
        recent_pipelines = [
            w for w in self.workflow_history[-10:] if w.get("type") == "pipeline"
        ]

        if not recent_pipelines:
            return {"trend": "no_data"}

        success_count = len(
            [w for w in recent_pipelines if w.get("status") == "success"]
        )
        avg_time = sum(w.get("execution_time", 0) for w in recent_pipelines) / len(
            recent_pipelines
        )

        return {
            "recent_success_rate": success_count / len(recent_pipelines),
            "recent_average_time": avg_time,
            "trend": (
                "improving" if success_count > len(recent_pipelines) * 0.7 else "stable"
            ),
        }

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

    async def process_pipeline_request(
        self,
        request_text: str,
        files: List[Dict] = None,
        auto_create: bool = True,
    ) -> Dict[str, Any]:
        """
        Process complex pipeline requests with enhanced capabilities.

        Args:
            request_text: User's natural language request
            files: List of uploaded files with metadata
            auto_create: Whether to auto-create missing agents

        Returns:
            Enhanced result with pipeline information
        """

        workflow_id = f"pipeline_{uuid.uuid4().hex[:8]}"

        try:
            if not self.is_backend_available():
                return {
                    "status": "error",
                    "workflow_id": workflow_id,
                    "error": "Backend pipeline orchestrator not available",
                }

            # Analyze request complexity
            complexity = await self._detect_request_complexity(request_text, files)

            # Process based on complexity
            if complexity in ["pipeline", "complex"]:
                result = await self._process_as_pipeline(
                    request_text, files, auto_create, workflow_id
                )
            else:
                # Use regular orchestrator for simple requests
                result = await self.process_user_request(
                    request_text, files, auto_create
                )

            # Add pipeline metadata
            if "metadata" not in result:
                result["metadata"] = {}
            result["metadata"]["complexity_detected"] = complexity
            result["metadata"]["pipeline_processing"] = complexity in [
                "pipeline",
                "complex",
            ]

            return result

        except Exception as e:
            return {
                "status": "error",
                "workflow_id": workflow_id,
                "error": f"Pipeline processing failed: {str(e)}",
            }

    async def _detect_request_complexity(
        self, request_text: str, files: List[Dict] = None
    ) -> str:
        """Detect complexity level of the request."""

        request_lower = request_text.lower()

        # Pipeline indicators
        pipeline_keywords = [
            "then",
            "after",
            "next",
            "followed by",
            "and then",
            "first",
            "second",
            "third",
            "finally",
            "last",
            "extract and",
            "analyze and",
            "process and",
            "create and",
            "step by step",
            "pipeline",
            "workflow",
            "sequence",
        ]

        # Complex indicators
        complex_keywords = [
            "multiple files",
            "compare",
            "merge",
            "combine",
            "different formats",
            "various sources",
            "cross-reference",
            "comprehensive",
            "detailed analysis",
            "full report",
        ]

        # Count indicators
        pipeline_count = sum(
            1 for keyword in pipeline_keywords if keyword in request_lower
        )
        complex_count = sum(
            1 for keyword in complex_keywords if keyword in request_lower
        )

        # Check for numbered steps
        step_indicators = ["1.", "2.", "3.", "step 1", "step 2", "step 3"]
        step_count = sum(
            1 for indicator in step_indicators if indicator in request_lower
        )

        # File complexity
        multiple_files = files and len(files) > 1

        # Decision logic
        if (
            complex_count > 0
            or (pipeline_count > 2)
            or step_count > 1
            or multiple_files
        ):
            return "complex"
        elif pipeline_count > 0 or len(request_lower.split()) > 20:
            return "pipeline"
        else:
            return "simple"

    async def _process_as_pipeline(
        self, request_text: str, files: List[Dict], auto_create: bool, workflow_id: str
    ) -> Dict[str, Any]:
        """Process request using pipeline orchestrator."""

        # Track workflow start
        self.active_workflows[workflow_id] = {
            "status": "processing",
            "started_at": datetime.now().isoformat(),
            "request": request_text,
            "files": len(files) if files else 0,
            "type": "pipeline",
        }

        try:
            # Step 1: Analyze complex request
            analysis_result = await self.pipeline_orchestrator.analyze_complex_request(
                request_text, files
            )

            if analysis_result["status"] != "success":
                return {
                    "status": "error",
                    "workflow_id": workflow_id,
                    "error": f"Pipeline analysis failed: {analysis_result.get('error')}",
                }

            # Step 2: Plan pipeline execution
            pipeline_plan = await self.pipeline_orchestrator.plan_pipeline(
                analysis_result, auto_create
            )

            # Step 3: Execute with monitoring
            execution_result = (
                await self.pipeline_orchestrator.execute_pipeline_with_adaptation(
                    pipeline_plan, request_text, files
                )
            )

            # Step 4: Generate response
            response = await self._generate_pipeline_response(
                request_text, execution_result, analysis_result
            )

            # Update workflow status
            final_status = execution_result.get("status", "unknown")
            self.active_workflows[workflow_id]["status"] = final_status
            self.active_workflows[workflow_id][
                "completed_at"
            ] = datetime.now().isoformat()

            # Add to history
            self.workflow_history.append(
                {
                    "workflow_id": workflow_id,
                    "request": request_text,
                    "status": final_status,
                    "type": "pipeline",
                    "started_at": self.active_workflows[workflow_id]["started_at"],
                    "completed_at": self.active_workflows[workflow_id]["completed_at"],
                    "execution_time": execution_result.get("execution_time", 0),
                    "files": len(files) if files else 0,
                    "steps_completed": execution_result.get("steps_completed", 0),
                    "total_steps": execution_result.get("total_steps", 0),
                }
            )

            return {
                "status": final_status,
                "workflow_id": workflow_id,
                "workflow": {
                    "type": "pipeline",
                    "steps": [
                        step.get("name", f"step_{i}")
                        for i, step in enumerate(pipeline_plan.get("steps", []))
                    ],
                    "execution_strategy": pipeline_plan.get(
                        "execution_strategy", "sequential"
                    ),
                    "total_steps": pipeline_plan.get("total_steps", 0),
                    "steps_completed": execution_result.get("steps_completed", 0),
                },
                "response": response,
                "results": execution_result.get("results", {}),
                "step_results": execution_result.get("step_results", {}),
                "metadata": {
                    "pipeline_analysis": analysis_result,
                    "execution_time": execution_result.get("execution_time", 0),
                    "adaptations": execution_result.get("adaptations", []),
                    "components_created": len(pipeline_plan.get("creation_needed", [])),
                    "performance_grade": self._calculate_performance_grade(
                        execution_result
                    ),
                },
                "errors": execution_result.get("errors", []),
            }

        except Exception as e:
            # Update workflow status
            self.active_workflows[workflow_id]["status"] = "error"
            self.active_workflows[workflow_id][
                "completed_at"
            ] = datetime.now().isoformat()

            return {
                "status": "error",
                "workflow_id": workflow_id,
                "error": f"Pipeline processing failed: {str(e)}",
            }

    async def _generate_pipeline_response(
        self, request_text: str, execution_result: Dict, analysis_result: Dict
    ) -> str:
        """Generate natural language response for pipeline execution."""

        steps_completed = execution_result.get("steps_completed", 0)
        total_steps = execution_result.get("total_steps", 0)
        adaptations = execution_result.get("adaptations", [])

        # Build response based on execution results
        if execution_result["status"] == "success":
            response_parts = [
                f"I successfully completed your {total_steps}-step request through an intelligent pipeline."
            ]

            # Summarize key results
            results = execution_result.get("results", {})
            if results:
                response_parts.append("Here's what I accomplished:")
                for step_name, result in results.items():
                    if result.get("status") == "success":
                        data = result.get("data", {})
                        if isinstance(data, dict) and data:
                            key_info = self._extract_key_result_info(data)
                            if key_info:
                                response_parts.append(f"- {step_name}: {key_info}")

            # Mention adaptations if any
            if adaptations:
                response_parts.append(
                    f"Note: I made {len(adaptations)} intelligent adaptations during processing to ensure optimal results."
                )

        elif execution_result["status"] == "partial":
            response_parts = [
                f"I completed {steps_completed} of {total_steps} steps in your pipeline request."
            ]

            # Mention what was accomplished
            successful_results = {
                k: v
                for k, v in execution_result.get("results", {}).items()
                if v.get("status") == "success"
            }
            if successful_results:
                response_parts.append("Successfully completed steps:")
                for step_name, result in successful_results.items():
                    data = result.get("data", {})
                    key_info = self._extract_key_result_info(data)
                    if key_info:
                        response_parts.append(f"- {step_name}: {key_info}")

            # Mention issues
            errors = execution_result.get("errors", [])
            if errors:
                response_parts.append(
                    f"Some steps encountered issues, but I provided the best possible results."
                )

        else:
            response_parts = [
                "I encountered difficulties processing your multi-step request.",
                "Please check the error details for more information.",
            ]

        return " ".join(response_parts)

    def _extract_key_result_info(self, data: Any) -> str:
        """Extract key information from result data for response generation."""

        if isinstance(data, dict):
            # Look for common result patterns
            if "count" in data:
                return f"found {data['count']} items"
            elif "total" in data:
                return f"processed {data['total']} items"
            elif "extracted" in data:
                extracted = data["extracted"]
                if isinstance(extracted, list):
                    return f"extracted {len(extracted)} items"
            elif "processed_data" in data:
                return "processed successfully"
            elif len(data) > 0:
                return f"generated {len(data)} results"

        elif isinstance(data, list):
            return f"generated {len(data)} items"

        elif isinstance(data, str) and data:
            return f"processed text ({len(data)} characters)"

        return "completed successfully"


# Global service instance
orchestrator_service = OrchestratorService()
