"""
Workflow Intelligence
Real-time monitoring and adaptation engine for pipeline execution
"""

import os
import sys
import json
import asyncio
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import openai

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    OPENAI_API_KEY,
    ORCHESTRATOR_MODEL,
    ORCHESTRATOR_MAX_TOKENS,
    PIPELINE_RECOVERY_PROMPT,
    WORKFLOW_ADAPTATION_PROMPT,
)
from core.registry import RegistryManager
from core.agent_factory import AgentFactory


class WorkflowIntelligence:
    """
    Real-time monitoring and adaptation engine for pipeline execution.
    Handles failure detection, recovery strategies, and workflow optimization.
    """

    def __init__(self, registry: RegistryManager):
        """Initialize the workflow intelligence engine."""
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        self.registry = registry
        self.agent_factory = AgentFactory()
        self.monitoring_data = []
        self.adaptation_history = []

    async def monitor_pipeline_execution(
        self, pipeline_state: Dict, step_result: Dict
    ) -> Dict[str, Any]:
        """
        Monitor pipeline execution and detect issues in real-time.

        Args:
            pipeline_state: Current pipeline state
            step_result: Result from latest step execution

        Returns:
            Monitoring analysis with recommendations
        """
        print(
            f"DEBUG: Monitoring pipeline step: {step_result.get('step_name', 'unknown')}"
        )

        # Record monitoring data
        monitoring_entry = {
            "pipeline_id": pipeline_state.get("pipeline_id"),
            "step_index": pipeline_state.get("current_step", 0),
            "step_name": step_result.get("step_name"),
            "status": step_result.get("status"),
            "timestamp": datetime.now().isoformat(),
            "execution_time": step_result.get("metadata", {}).get("execution_time", 0),
        }
        self.monitoring_data.append(monitoring_entry)

        # Analyze step result
        analysis = {
            "status": "healthy",
            "issues_detected": [],
            "recommendations": [],
            "adaptation_needed": False,
            "adaptation_strategy": None,
        }

        # Check for failures
        if step_result.get("status") == "error":
            analysis["status"] = "failed"
            analysis["issues_detected"].append(
                {
                    "type": "step_failure",
                    "description": step_result.get("error", "Unknown error"),
                    "severity": "high",
                }
            )
            analysis["adaptation_needed"] = True

        # Check for performance issues
        exec_time = monitoring_entry["execution_time"]
        if exec_time > 30:  # Configurable threshold
            analysis["issues_detected"].append(
                {
                    "type": "performance_degradation",
                    "description": f"Step took {exec_time:.1f}s (threshold: 30s)",
                    "severity": "medium",
                }
            )

        # Check data quality issues
        data_quality_issues = self._analyze_data_quality(step_result)
        analysis["issues_detected"].extend(data_quality_issues)

        # Generate recommendations
        if analysis["issues_detected"]:
            recommendations = await self._generate_recommendations(
                analysis["issues_detected"], pipeline_state, step_result
            )
            analysis["recommendations"] = recommendations

            # Determine if adaptation is needed
            if any(
                issue["severity"] == "high" for issue in analysis["issues_detected"]
            ):
                analysis["adaptation_needed"] = True
                analysis["adaptation_strategy"] = await self._plan_adaptation_strategy(
                    analysis["issues_detected"], pipeline_state, step_result
                )

        print(
            f"DEBUG: Monitoring analysis - Status: {analysis['status']}, Issues: {len(analysis['issues_detected'])}"
        )
        return analysis

    def _analyze_data_quality(self, step_result: Dict) -> List[Dict]:
        """Analyze data quality issues in step results."""
        issues = []

        data = step_result.get("data", {})

        # Check for empty results
        if not data or (isinstance(data, (list, dict)) and len(data) == 0):
            issues.append(
                {
                    "type": "empty_results",
                    "description": "Step produced no data",
                    "severity": "medium",
                }
            )

        # Check for null/undefined values
        if isinstance(data, dict):
            null_fields = [k for k, v in data.items() if v is None]
            if null_fields:
                issues.append(
                    {
                        "type": "null_values",
                        "description": f"Fields with null values: {null_fields}",
                        "severity": "low",
                    }
                )

        # Check for data type inconsistencies
        if isinstance(data, list) and data:
            first_type = type(data[0])
            if not all(isinstance(item, first_type) for item in data):
                issues.append(
                    {
                        "type": "type_inconsistency",
                        "description": "Mixed data types in result list",
                        "severity": "medium",
                    }
                )

        return issues

    async def _generate_recommendations(
        self, issues: List[Dict], pipeline_state: Dict, step_result: Dict
    ) -> List[Dict]:
        """Generate recommendations for detected issues."""
        recommendations = []

        for issue in issues:
            if issue["type"] == "step_failure":
                recommendations.append(
                    {
                        "type": "retry_with_different_agent",
                        "description": "Try executing with a different agent or create replacement",
                        "priority": "high",
                    }
                )
                recommendations.append(
                    {
                        "type": "modify_input_data",
                        "description": "Preprocess input data to handle edge cases",
                        "priority": "medium",
                    }
                )

            elif issue["type"] == "performance_degradation":
                recommendations.append(
                    {
                        "type": "optimize_agent",
                        "description": "Consider creating optimized version of agent",
                        "priority": "medium",
                    }
                )

            elif issue["type"] == "empty_results":
                recommendations.append(
                    {
                        "type": "verify_input_data",
                        "description": "Check if input data is suitable for processing",
                        "priority": "high",
                    }
                )
                recommendations.append(
                    {
                        "type": "adjust_agent_logic",
                        "description": "Modify agent to handle edge cases better",
                        "priority": "medium",
                    }
                )

        return recommendations

    async def _plan_adaptation_strategy(
        self, issues: List[Dict], pipeline_state: Dict, step_result: Dict
    ) -> Dict[str, Any]:
        """Plan adaptation strategy for handling issues."""

        # Use GPT-4 to plan intelligent adaptation
        prompt = WORKFLOW_ADAPTATION_PROMPT.format(
            issues=json.dumps(issues),
            pipeline_state=json.dumps(
                {
                    "current_step": pipeline_state.get("current_step"),
                    "total_steps": pipeline_state.get("total_steps"),
                    "previous_results": pipeline_state.get("step_results", {}),
                }
            ),
            step_result=json.dumps(
                {
                    "status": step_result.get("status"),
                    "error": step_result.get("error"),
                    "agent_name": step_result.get("agent_name"),
                }
            ),
        )

        try:
            response = await self._call_gpt4_json(
                system_prompt="Plan intelligent adaptation strategies for workflow issues.",
                user_prompt=prompt,
            )

            strategy = json.loads(response)
            strategy["generated_at"] = datetime.now().isoformat()

            return strategy

        except Exception as e:
            print(f"DEBUG: Adaptation planning failed: {str(e)}")
            return {
                "action": "manual_intervention",
                "reason": f"Automated planning failed: {str(e)}",
                "generated_at": datetime.now().isoformat(),
            }

    async def execute_adaptation(
        self, adaptation_strategy: Dict, pipeline_state: Dict, step_plan: Dict
    ) -> Dict[str, Any]:
        """
        Execute adaptation strategy to recover from issues.

        Args:
            adaptation_strategy: Strategy from _plan_adaptation_strategy
            pipeline_state: Current pipeline state
            step_plan: Plan for the failed step

        Returns:
            Adaptation execution result
        """
        print(
            f"DEBUG: Executing adaptation strategy: {adaptation_strategy.get('action', 'unknown')}"
        )

        adaptation_result = {
            "status": "failed",
            "action_taken": adaptation_strategy.get("action"),
            "timestamp": datetime.now().isoformat(),
            "details": {},
        }

        action = adaptation_strategy.get("action", "")

        try:
            if action == "create_replacement_agent":
                # Create new agent to replace failed one
                result = await self._create_replacement_agent(
                    adaptation_strategy, step_plan
                )
                adaptation_result.update(result)

            elif action == "modify_existing_agent":
                # Modify existing agent
                result = await self._modify_existing_agent(
                    adaptation_strategy, step_plan
                )
                adaptation_result.update(result)

            elif action == "retry_with_preprocessing":
                # Add data preprocessing step
                result = await self._add_preprocessing_step(
                    adaptation_strategy, step_plan, pipeline_state
                )
                adaptation_result.update(result)

            elif action == "skip_step_with_fallback":
                # Skip problematic step and use fallback
                result = self._create_fallback_result(adaptation_strategy, step_plan)
                adaptation_result.update(result)

            else:
                adaptation_result["status"] = "unsupported"
                adaptation_result["details"][
                    "message"
                ] = f"Unsupported adaptation action: {action}"

            # Record adaptation
            self.adaptation_history.append(adaptation_result.copy())

        except Exception as e:
            adaptation_result["status"] = "error"
            adaptation_result["details"]["error"] = str(e)
            print(f"DEBUG: Adaptation execution failed: {str(e)}")

        return adaptation_result

    async def _create_replacement_agent(
        self, adaptation_strategy: Dict, step_plan: Dict
    ) -> Dict[str, Any]:
        """Create replacement agent for failed step."""

        replacement_spec = adaptation_strategy.get("replacement_spec", {})

        # Use agent factory to create replacement
        creation_result = self.agent_factory.create_pipeline_agent(
            {
                "name": replacement_spec.get(
                    "name", f"replacement_{step_plan.get('name', 'agent')}"
                ),
                "description": replacement_spec.get(
                    "description", f"Replacement for {step_plan.get('name')}"
                ),
                "required_tools": replacement_spec.get("tools", []),
                "pipeline_context": step_plan.get("pipeline_context", {}),
            }
        )

        if creation_result["status"] == "success":
            return {
                "status": "success",
                "details": {
                    "replacement_agent": replacement_spec.get("name"),
                    "creation_result": creation_result,
                },
            }
        else:
            return {
                "status": "failed",
                "details": {
                    "creation_error": creation_result.get("message", "Unknown error")
                },
            }

    async def _modify_existing_agent(
        self, adaptation_strategy: Dict, step_plan: Dict
    ) -> Dict[str, Any]:
        """Modify existing agent to handle issues."""

        # For now, create a modified version instead of modifying in-place
        modifications = adaptation_strategy.get("modifications", {})
        original_agent = step_plan.get("agent_assigned")

        modified_spec = {
            "name": f"{original_agent}_modified",
            "description": f"Modified version of {original_agent}",
            "modifications": modifications,
            "original_agent": original_agent,
        }

        creation_result = self.agent_factory.create_pipeline_agent(modified_spec)

        if creation_result["status"] == "success":
            return {
                "status": "success",
                "details": {
                    "modified_agent": modified_spec["name"],
                    "modifications": modifications,
                },
            }
        else:
            return {
                "status": "failed",
                "details": {
                    "modification_error": creation_result.get(
                        "message", "Unknown error"
                    )
                },
            }

    async def _add_preprocessing_step(
        self, adaptation_strategy: Dict, step_plan: Dict, pipeline_state: Dict
    ) -> Dict[str, Any]:
        """Add preprocessing step to handle data issues."""

        preprocessing_spec = adaptation_strategy.get("preprocessing_spec", {})

        # Create preprocessing agent
        creation_result = self.agent_factory.create_pipeline_agent(
            {
                "name": f"preprocessor_{step_plan.get('name', 'data')}",
                "description": f"Preprocessor for {step_plan.get('name')}",
                "required_tools": preprocessing_spec.get(
                    "tools", ["clean_data", "validate_data"]
                ),
                "preprocessing": True,
            }
        )

        if creation_result["status"] == "success":
            return {
                "status": "success",
                "details": {
                    "preprocessing_agent": f"preprocessor_{step_plan.get('name', 'data')}",
                    "preprocessing_spec": preprocessing_spec,
                },
            }
        else:
            return {
                "status": "failed",
                "details": {
                    "preprocessing_error": creation_result.get(
                        "message", "Unknown error"
                    )
                },
            }

    def _create_fallback_result(
        self, adaptation_strategy: Dict, step_plan: Dict
    ) -> Dict[str, Any]:
        """Create fallback result for skipped step."""

        fallback_data = adaptation_strategy.get("fallback_data", {})

        return {
            "status": "success",
            "details": {
                "action": "step_skipped",
                "fallback_data": fallback_data,
                "reason": "Created fallback result due to persistent failures",
            },
            "fallback_result": {
                "status": "success",
                "data": fallback_data,
                "metadata": {
                    "fallback": True,
                    "original_step": step_plan.get("name"),
                    "reason": "Adaptation strategy - step skipped with fallback",
                },
            },
        }

    def analyze_pipeline_performance(self, pipeline_id: str) -> Dict[str, Any]:
        """Analyze overall pipeline performance."""

        # Get monitoring data for this pipeline
        pipeline_data = [
            entry
            for entry in self.monitoring_data
            if entry.get("pipeline_id") == pipeline_id
        ]

        if not pipeline_data:
            return {"status": "no_data", "pipeline_id": pipeline_id}

        # Calculate metrics
        total_time = sum(entry.get("execution_time", 0) for entry in pipeline_data)
        step_count = len(pipeline_data)
        failed_steps = len(
            [entry for entry in pipeline_data if entry.get("status") == "error"]
        )

        analysis = {
            "pipeline_id": pipeline_id,
            "total_execution_time": total_time,
            "total_steps": step_count,
            "failed_steps": failed_steps,
            "success_rate": (
                (step_count - failed_steps) / step_count if step_count > 0 else 0
            ),
            "average_step_time": total_time / step_count if step_count > 0 else 0,
            "performance_grade": "unknown",
        }

        # Assign performance grade
        if analysis["success_rate"] >= 0.9 and analysis["average_step_time"] < 10:
            analysis["performance_grade"] = "excellent"
        elif analysis["success_rate"] >= 0.8 and analysis["average_step_time"] < 20:
            analysis["performance_grade"] = "good"
        elif analysis["success_rate"] >= 0.6:
            analysis["performance_grade"] = "acceptable"
        else:
            analysis["performance_grade"] = "poor"

        return analysis

    def get_adaptation_history(self) -> List[Dict]:
        """Get history of adaptations performed."""
        return self.adaptation_history.copy()

    def clear_monitoring_data(self, older_than_hours: int = 24):
        """Clear old monitoring data."""
        cutoff_time = datetime.now() - timedelta(hours=older_than_hours)

        self.monitoring_data = [
            entry
            for entry in self.monitoring_data
            if datetime.fromisoformat(entry["timestamp"]) > cutoff_time
        ]

        self.adaptation_history = [
            entry
            for entry in self.adaptation_history
            if datetime.fromisoformat(entry["timestamp"]) > cutoff_time
        ]

    async def _call_gpt4_json(
        self, system_prompt: str, user_prompt: str, temperature: float = 0.1
    ) -> str:
        """Call GPT-4 for JSON responses."""
        enhanced_prompt = f"{system_prompt}\n\n{user_prompt}\n\nRespond with ONLY valid JSON, no other text."

        response = self.client.chat.completions.create(
            model=ORCHESTRATOR_MODEL,
            max_completion_tokens=ORCHESTRATOR_MAX_TOKENS,
            messages=[{"role": "user", "content": enhanced_prompt}],
        )

        content = response.choices[0].message.content

        # Extract JSON from response
        if "```json" in content:
            start = content.find("```json") + 7
            end = content.find("```", start)
            if end > start:
                return content[start:end].strip()
        elif "{" in content:
            start = content.find("{")
            end = content.rfind("}") + 1
            if end > start:
                return content[start:end].strip()

        return content.strip()
