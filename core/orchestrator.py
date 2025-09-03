"""
GPT-4 Orchestrator
Intelligent workflow planning and agent selection using GPT-4
"""

import os
import sys
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import openai

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    OPENAI_API_KEY,
    ORCHESTRATOR_MODEL,
    ORCHESTRATOR_TEMPERATURE,
    ORCHESTRATOR_SYSTEM_PROMPT,
)
from core.registry import RegistryManager
from core.workflow_engine import WorkflowEngine
from core.agent_factory import AgentFactory
from core.tool_factory import ToolFactory


class Orchestrator:
    def __init__(self):
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        self.registry = RegistryManager()
        self.workflow_engine = WorkflowEngine()
        self.agent_factory = AgentFactory()
        self.tool_factory = ToolFactory()

    def process_request(
        self,
        user_request: str,
        files: List[Dict[str, Any]] = None,
        auto_create: bool = False,
    ) -> Dict[str, Any]:
        """
        Process a user request by planning and executing the appropriate workflow.

        Args:
            user_request: Natural language request from user
            files: Optional list of file information
            auto_create: Whether to automatically create missing agents/tools

        Returns:
            Dict containing workflow results and execution details
        """

        print("\n[ORCHESTRATOR] Analyzing request...")

        # Step 1: Analyze request and plan workflow
        workflow_plan = self._plan_workflow(user_request, files)

        if workflow_plan["status"] == "error":
            return {
                "status": "error",
                "message": workflow_plan["message"],
                "timestamp": datetime.now().isoformat(),
            }

        print(
            f"[ORCHESTRATOR] Planned workflow: {' -> '.join(workflow_plan['workflow_steps'])}"
        )

        # Step 2: Check for missing capabilities
        if workflow_plan.get("missing_agents") or workflow_plan.get("missing_tools"):
            print("[ORCHESTRATOR] Missing capabilities detected")

            if auto_create:
                # Try to create missing components
                creation_result = self._create_missing_components(
                    workflow_plan.get("missing_agents", []),
                    workflow_plan.get("missing_tools", []),
                )

                if not creation_result["success"]:
                    return {
                        "status": "error",
                        "message": f"Failed to create required components: {creation_result['message']}",
                        "missing": {
                            "agents": workflow_plan.get("missing_agents", []),
                            "tools": workflow_plan.get("missing_tools", []),
                        },
                    }
            else:
                # Return what's missing
                return {
                    "status": "missing_capabilities",
                    "message": "Required agents or tools are not available",
                    "missing": {
                        "agents": workflow_plan.get("missing_agents", []),
                        "tools": workflow_plan.get("missing_tools", []),
                    },
                    "suggestion": "Enable auto_create to automatically build missing components",
                }

        # Step 3: Prepare initial data
        initial_data = self._prepare_initial_data(user_request, files, workflow_plan)

        # Step 4: Execute workflow
        print("[ORCHESTRATOR] Executing workflow...")

        try:
            workflow_result = self.workflow_engine.create_and_execute(
                agent_sequence=workflow_plan["workflow_steps"],
                initial_data=initial_data,
                workflow_id=workflow_plan.get("workflow_id"),
            )

            # Step 5: Synthesize results
            print("[ORCHESTRATOR] Synthesizing results...")
            final_response = self._synthesize_results(
                user_request, workflow_result, workflow_plan
            )

            return {
                "status": "success",
                "response": final_response,
                "workflow": {
                    "steps": workflow_plan["workflow_steps"],
                    "execution_path": workflow_result.get("execution_path", []),
                    "workflow_id": workflow_plan.get("workflow_id"),
                },
                "raw_results": workflow_result.get("results", {}),
                "errors": workflow_result.get("errors", []),
                "timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Workflow execution failed: {str(e)}",
                "workflow": workflow_plan,
                "timestamp": datetime.now().isoformat(),
            }

    def _plan_workflow(self, user_request: str, files=None) -> Dict:
        """Two-phase planning: Analysis then structured plan."""

        # Phase 1: Analyze request
        analysis = self._analyze_request(user_request, files)

        # Phase 2: Create structured plan
        agents = self.registry.list_agents()
        tools = self.registry.list_tools()

        # Format for planning prompt
        from config import ORCHESTRATOR_PLANNING_PROMPT

        planning_prompt = ORCHESTRATOR_PLANNING_PROMPT.format(analysis=analysis)

        try:
            response = self.client.chat.completions.create(
                model=ORCHESTRATOR_MODEL,
                temperature=0.1,
                response_format={"type": "json_object"},
                messages=[
                    {
                        "role": "system",
                        "content": "You are a workflow planner. Output only valid JSON.",
                    },
                    {"role": "user", "content": planning_prompt},
                ],
            )

            plan = json.loads(response.choices[0].message.content)

            # Handle missing capabilities
            if plan.get("missing_capabilities"):
                if (
                    plan["missing_capabilities"]["agents"]
                    or plan["missing_capabilities"]["tools"]
                ):
                    # Create missing components
                    creation_result = self._create_missing_components(
                        plan["missing_capabilities"]["agents"],
                        plan["missing_capabilities"]["tools"],
                    )

                    # Update plan with created components
                    if creation_result["success"]:
                        # Re-plan with new components
                        return self._plan_workflow(user_request, files)

            plan["status"] = "success"
            return plan

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _synthesize_results(
        self,
        user_request: str,
        workflow_result: Dict[str, Any],
        workflow_plan: Dict[str, Any],
    ) -> str:
        """
        Use GPT-4 to synthesize results into a coherent response.

        Args:
            user_request: Original user request
            workflow_result: Raw results from workflow execution
            workflow_plan: The planned workflow

        Returns:
            Natural language response summarizing the results
        """

        # Format results for GPT-4
        results_summary = self._format_results_for_synthesis(workflow_result)

        prompt = f"""Synthesize the following workflow results into a clear, helpful response for the user.

ORIGINAL REQUEST: {user_request}

WORKFLOW EXECUTED: {' -> '.join(workflow_plan['workflow_steps'])}

RESULTS:
{results_summary}

Provide a natural language response that:
1. Directly answers the user's request
2. Highlights key findings
3. Mentions any important details or patterns
4. Notes any errors or limitations if present

Keep the response concise but comprehensive.
"""

        try:
            response = self.client.chat.completions.create(
                model=ORCHESTRATOR_MODEL,
                temperature=0.5,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant synthesizing workflow results.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )

            return response.choices[0].message.content

        except Exception as e:
            # Fallback to basic summary
            return self._create_basic_summary(workflow_result)

    def _prepare_initial_data(
        self,
        user_request: str,
        files: List[Dict[str, Any]],
        workflow_plan: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Prepare initial data for workflow execution.

        Args:
            user_request: User's request
            files: File information
            workflow_plan: Planned workflow

        Returns:
            Initial data dictionary for workflow
        """

        initial_data = {
            "request": user_request,
            "files": files or [],
            "workflow_plan": workflow_plan,
        }

        # Add file paths if files provided
        if files and len(files) > 0:
            initial_data["file_path"] = files[0].get("path", "")
            initial_data["file_type"] = files[0].get("type", "")

        # Add any extracted text directly if it's a simple text request
        if not files and isinstance(user_request, str):
            # Check if the request contains data to process
            if ":" in user_request or "\n" in user_request:
                # Might contain embedded data
                parts = user_request.split(":", 1)
                if len(parts) > 1:
                    initial_data["text"] = parts[1].strip()
                else:
                    initial_data["text"] = user_request
            else:
                initial_data["text"] = user_request

        return initial_data

    def _build_planning_context(
        self, agents: List[Dict], tools: List[Dict], files: List[Dict]
    ) -> str:
        """Build context string for planning."""

        context = f"Agents: {len(agents)}, Tools: {len(tools)}"
        if files:
            context += f", Files: {len(files)}"
            for file in files:
                context += f" [{file.get('type', 'unknown')}]"
        return context

    def _format_agents_list(self, agents: List[Dict]) -> str:
        """Format agents list for prompt."""

        formatted = []
        for agent in agents:
            formatted.append(
                f"- {agent['name']}: {agent['description']} "
                f"(uses: {', '.join(agent.get('uses_tools', []))})"
            )
        return "\n".join(formatted) if formatted else "No agents available"

    def _format_tools_list(self, tools: List[Dict]) -> str:
        """Format tools list for prompt."""

        formatted = []
        for tool in tools[:10]:  # Limit to prevent prompt overflow
            formatted.append(f"- {tool['name']}: {tool['description']}")

        if len(tools) > 10:
            formatted.append(f"... and {len(tools) - 10} more tools")

        return "\n".join(formatted) if formatted else "No tools available"

    def _validate_workflow_plan(
        self, plan: Dict[str, Any], available_agents: List[Dict]
    ) -> Dict[str, Any]:
        """
        Validate and clean the workflow plan.

        Args:
            plan: Raw plan from GPT-4
            available_agents: List of available agents

        Returns:
            Validated and cleaned plan
        """

        # Ensure required keys exist
        if "workflow_steps" not in plan:
            plan["workflow_steps"] = []
        if "missing_agents" not in plan:
            plan["missing_agents"] = []
        if "missing_tools" not in plan:
            plan["missing_tools"] = []

        # Get available agent names
        available_names = [a["name"] for a in available_agents]

        # Validate workflow steps
        valid_steps = []
        for step in plan["workflow_steps"]:
            if step in available_names:
                valid_steps.append(step)
            else:
                # Move to missing agents if not available
                if step not in plan["missing_agents"]:
                    plan["missing_agents"].append(step)

        plan["workflow_steps"] = valid_steps

        return plan

    def _format_results_for_synthesis(self, workflow_result: Dict[str, Any]) -> str:
        """Format workflow results for synthesis."""

        formatted = []

        for agent_name, result in workflow_result.get("results", {}).items():
            formatted.append(f"\n[{agent_name}]")

            if isinstance(result, dict):
                if "status" in result:
                    formatted.append(f"Status: {result['status']}")

                if "data" in result and result["data"]:
                    # Format data nicely
                    data_str = json.dumps(result["data"], indent=2)
                    if len(data_str) > 500:
                        data_str = data_str[:500] + "..."
                    formatted.append(f"Data: {data_str}")

        if workflow_result.get("errors"):
            formatted.append("\nERRORS:")
            for error in workflow_result["errors"]:
                formatted.append(
                    f"- {error.get('agent', 'unknown')}: {error.get('error', '')}"
                )

        return "\n".join(formatted)

    def _create_basic_summary(self, workflow_result: Dict[str, Any]) -> str:
        """Create a basic summary without GPT-4."""

        summary = ["Workflow execution completed."]

        # Add results summary
        for agent_name, result in workflow_result.get("results", {}).items():
            if isinstance(result, dict) and result.get("status") == "success":
                summary.append(f"- {agent_name}: Completed successfully")

                if "data" in result:
                    # Add key data points
                    data = result["data"]
                    if isinstance(data, dict):
                        for key in list(data.keys())[:3]:  # First 3 keys
                            summary.append(f"  - {key}: {data[key]}")

        # Add errors
        if workflow_result.get("errors"):
            summary.append("\nErrors encountered:")
            for error in workflow_result["errors"]:
                summary.append(f"- {error.get('error', 'Unknown error')}")

        return "\n".join(summary)

    def _generate_workflow_id(self) -> str:
        """Generate unique workflow ID."""

        import random

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = random.randint(1000, 9999)
        return f"orch_{timestamp}_{random_suffix}"

    def _create_missing_components(
        self, missing_agents: List, missing_tools: List
    ) -> Dict:
        """Create missing components using GPT-4 + Claude."""

        created = {"agents": [], "tools": []}

        # Create tools first
        for tool_spec in missing_tools:
            if isinstance(tool_spec, dict):
                name = tool_spec.get("name", "unknown_tool")
                purpose = tool_spec.get("purpose", "Process data")

                # Use GPT-4 to design the tool
                tool_design = self._design_component("tool", name, purpose)

                # Use Claude to implement
                result = self.tool_factory.create_tool(
                    tool_name=name,
                    description=purpose,
                    input_description=tool_design.get("input", "Any input"),
                    output_description=tool_design.get("output", "Processed output"),
                )

                if result["status"] == "success":
                    created["tools"].append(name)

        # Create agents
        for agent_spec in missing_agents:
            if isinstance(agent_spec, dict):
                name = agent_spec.get("name", "unknown_agent")
                purpose = agent_spec.get("purpose", "Process data")
                tools = agent_spec.get("tools_needed", [])

                # Design agent
                agent_design = self._design_component("agent", name, purpose)

                # Implement
                result = self.agent_factory.create_agent(
                    agent_name=name,
                    description=purpose,
                    required_tools=tools,
                    input_description=agent_design.get("input", "Flexible input"),
                    output_description=agent_design.get("output", "Structured output"),
                    workflow_steps=agent_design.get("steps", []),
                )

                if result["status"] == "success":
                    created["agents"].append(name)

        return {
            "success": True,
            "created_agents": created["agents"],
            "created_tools": created["tools"],
        }

    def _analyze_request(self, user_request: str, files) -> str:
        """Analyze request to understand intent."""

        from config import ORCHESTRATOR_ANALYSIS_PROMPT

        # Get available components
        agents = self.registry.list_agents()
        tools = self.registry.list_tools()

        agents_desc = "\n".join(
            [
                f"- {a['name']}: {a['description']} (uses: {', '.join(a.get('uses_tools', []))})"
                for a in agents
            ]
        )

        tools_desc = "\n".join(
            [
                f"- {t['name']}: {t['description']}"
                for t in tools[:20]  # Limit for context
            ]
        )

        prompt = ORCHESTRATOR_ANALYSIS_PROMPT.format(
            request=user_request,
            files=json.dumps(files) if files else "None",
            available_agents=agents_desc,
            available_tools=tools_desc,
        )

        response = self.client.chat.completions.create(
            model=ORCHESTRATOR_MODEL,
            temperature=0.3,
            messages=[
                {
                    "role": "system",
                    "content": "Analyze the request and available capabilities.",
                },
                {"role": "user", "content": prompt},
            ],
        )

        return response.choices[0].message.content

    def _execute_workflow(self, plan: Dict, initial_data: Dict) -> Dict:
        """Execute workflow based on type."""

        workflow_type = plan.get("workflow_type", "sequential")

        if workflow_type == "parallel":
            # Extract parallel agents
            agents = [step["agent"] for step in plan["workflow_steps"]]
            workflow = self.workflow_engine.create_parallel_workflow(agents)
        elif workflow_type == "conditional":
            workflow = self.workflow_engine.create_conditional_workflow(plan)
        else:  # sequential
            agents = [step["agent"] for step in plan["workflow_steps"]]
            workflow = self.workflow_engine.create_workflow(agents)

        # Execute with proper state management
        return self.workflow_engine.execute_workflow(workflow, initial_data)

    def _design_component(self, component_type: str, name: str, purpose: str) -> Dict:
        """Use GPT-4 to design component specifications."""

        prompt = f"""Design a {component_type} with these requirements:
        Name: {name}
        Purpose: {purpose}
        
        Provide:
        - Input description
        - Output description
        - Processing steps
        - Required capabilities
        
        Output as JSON."""

        response = self.client.chat.completions.create(
            model=ORCHESTRATOR_MODEL,
            temperature=0.3,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "Design component specifications."},
                {"role": "user", "content": prompt},
            ],
        )

        return json.loads(response.choices[0].message.content)


class OrchestratorCLI:
    """Command-line interface for testing the orchestrator."""

    def __init__(self):
        self.orchestrator = Orchestrator()

    def run(self):
        """Run interactive orchestrator session."""

        print("\n" + "=" * 50)
        print("GPT-4 ORCHESTRATOR - Natural Language Interface")
        print("=" * 50)

        print("\nEnter your request in natural language.")
        print("Examples:")
        print("  - Extract all emails from this text: Contact john@example.com")
        print("  - Analyze these numbers and calculate statistics: 10, 20, 30, 40, 50")
        print("  - Process this document and extract key information")

        while True:
            print("\n" + "-" * 40)
            user_request = input("\nYour request (or 'quit'): ").strip()

            if user_request.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break

            if not user_request:
                continue

            # Check for file reference
            files = None
            if "file:" in user_request.lower():
                # Extract file path
                parts = user_request.split("file:", 1)
                if len(parts) > 1:
                    file_path = parts[1].strip().split()[0]
                    files = [{"path": file_path, "type": "unknown"}]
                    user_request = parts[0].strip()

            # Process the request
            print("\nProcessing...")
            result = self.orchestrator.process_request(
                user_request=user_request, files=files, auto_create=False
            )

            # Display results
            print("\n" + "=" * 50)
            print("RESULTS")
            print("=" * 50)

            if result["status"] == "success":
                print(f"\nResponse:\n{result['response']}")

                if result.get("workflow"):
                    print(
                        f"\nWorkflow executed: {' -> '.join(result['workflow']['steps'])}"
                    )

                if result.get("errors"):
                    print("\nErrors encountered:")
                    for error in result["errors"]:
                        print(f"  - {error}")

            elif result["status"] == "missing_capabilities":
                print(f"\nMissing capabilities detected:")
                if result["missing"]["agents"]:
                    print(f"  Missing agents: {', '.join(result['missing']['agents'])}")
                if result["missing"]["tools"]:
                    print(f"  Missing tools: {', '.join(result['missing']['tools'])}")
                print(
                    "\nSuggestion: Enable auto_create mode to build these automatically"
                )

            else:
                print(f"\nError: {result.get('message', 'Unknown error')}")


if __name__ == "__main__":
    cli = OrchestratorCLI()
    cli.run()
