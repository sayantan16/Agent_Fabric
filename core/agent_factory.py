"""
Agent Factory
Dynamically generates agent code using Claude API
"""

import os
import sys
import ast
import json
from typing import Dict, Optional, List
from anthropic import Anthropic

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (
    ANTHROPIC_API_KEY,
    CLAUDE_AGENT_GENERATION_PROMPT,
    CLAUDE_MODEL,
    CLAUDE_TEMPERATURE,
    MIN_AGENT_LINES,
    MAX_AGENT_LINES,
    ALLOWED_IMPORTS,
    EXAMPLE_AGENT_TEMPLATE,
)
from core.registry import RegistryManager
from core.tool_factory import ToolFactory


class AgentFactory:
    def __init__(self):
        self.client = Anthropic(api_key=ANTHROPIC_API_KEY)
        self.registry = RegistryManager()
        self.tool_factory = ToolFactory()
        self.allowed_imports = ALLOWED_IMPORTS

    def create_agent(
        self,
        agent_name: str,
        description: str,
        required_tools: List[str],
        input_description: str,
        output_description: str,
        workflow_steps: List[str] = None,
    ) -> Dict:
        """
        Create a new agent using Claude.

        Args:
            agent_name: Name of the agent function
            description: What the agent does
            required_tools: List of tools the agent should use
            input_description: Description of expected input
            output_description: Description of expected output
            workflow_steps: Optional list of steps the agent should perform

        Returns:
            Dict with status and generated code or error
        """

        # Check if agent already exists
        if self.registry.agent_exists(agent_name):
            return {
                "status": "exists",
                "message": f"Agent '{agent_name}' already exists in registry",
            }

        # Check if required tools exist
        missing_tools = []
        for tool in required_tools:
            if not self.registry.tool_exists(tool):
                missing_tools.append(tool)

        if missing_tools:
            return {
                "status": "error",
                "message": f"Missing required tools: {', '.join(missing_tools)}",
                "missing_tools": missing_tools,
            }

        # Build the prompt
        prompt = self._build_agent_prompt(
            agent_name,
            description,
            required_tools,
            input_description,
            output_description,
            workflow_steps,
        )

        try:
            # Call Claude API
            response = self.client.messages.create(
                model=CLAUDE_MODEL,
                temperature=CLAUDE_TEMPERATURE,
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}],
            )

            # Extract code from response
            code = self._extract_code_from_response(response.content[0].text)

            if not code:
                return {
                    "status": "error",
                    "message": "No valid Python code found in response",
                }

            # Validate the generated code
            validation_result = self._validate_agent_code(code, agent_name)

            if validation_result["valid"]:
                # Determine input/output schemas
                input_schema = {"data": "any"}
                output_schema = {"data": "any"}

                # Register the agent
                self.registry.register_agent(
                    name=agent_name,
                    description=description,
                    code=code,
                    uses_tools=required_tools,
                    input_schema=input_schema,
                    output_schema=output_schema,
                    tags=self._extract_tags(description),
                )

                return {
                    "status": "success",
                    "code": code,
                    "message": f"Agent '{agent_name}' created successfully",
                    "line_count": len(code.splitlines()),
                }
            else:
                return {
                    "status": "error",
                    "message": validation_result["error"],
                    "code": code,
                }

        except Exception as e:
            return {"status": "error", "message": f"API error: {str(e)}"}

    def _build_agent_prompt(
        self,
        agent_name: str,
        description: str,
        required_tools: List[str],
        input_desc: str,
        output_desc: str,
        workflow_steps: List[str],
    ) -> str:
        """Build the prompt for Claude to generate agent code."""

        # Get tool signatures for reference
        tool_info = []
        for tool_name in required_tools:
            tool = self.registry.get_tool(tool_name)
            if tool:
                tool_info.append(f"- {tool_name}: {tool['description']}")

        prompt = CLAUDE_AGENT_GENERATION_PROMPT.format(
            agent_name=agent_name,
            min_lines=MIN_AGENT_LINES,
            max_lines=MAX_AGENT_LINES,
            allowed_imports=", ".join(self.allowed_imports),
            template=EXAMPLE_AGENT_TEMPLATE,
        )

        prompt += f"""
    SPECIFIC AGENT DETAILS:
    - Description: {description}
    - Required Tools: {chr(10).join(tool_info)}
    - Expected Input: {input_desc}
    - Expected Output: {output_desc}
    """

        if workflow_steps:
            prompt += f"""
    WORKFLOW STEPS:
    {chr(10).join(f'{i+1}. {step}' for i, step in enumerate(workflow_steps))}
    """

        return prompt

    def _extract_code_from_response(self, response: str) -> Optional[str]:
        """Extract Python code from Claude's response."""

        # Remove markdown code blocks if present
        if "```python" in response:
            start = response.find("```python") + 9
            end = response.find("```", start)
            code = response[start:end].strip()
        elif "```" in response:
            start = response.find("```") + 3
            end = response.find("```", start)
            code = response[start:end].strip()
        else:
            # Assume entire response is code
            code = response.strip()

        # Verify it starts with 'def'
        if not code.startswith("def "):
            # Try to find where def starts
            def_index = code.find("def ")
            if def_index != -1:
                code = code[def_index:]

        return code if code.startswith("def ") else None

    def _validate_agent_code(self, code: str, expected_base_name: str) -> Dict:
        """Enhanced validation for flexible agents."""

        try:
            # Parse syntax
            tree = ast.parse(code)

            # Basic checks
            if not isinstance(tree.body[0], ast.FunctionDef):
                return {"valid": False, "error": "Not a function"}

            # Check name
            func_name = tree.body[0].name
            if not (
                func_name == f"{expected_base_name}_agent"
                or func_name == expected_base_name
            ):
                return {"valid": False, "error": f"Wrong function name: {func_name}"}

            # Check for required patterns
            from config import AGENT_VALIDATION_RULES

            for pattern in AGENT_VALIDATION_RULES["required_patterns"]:
                if pattern not in code:
                    return {
                        "valid": False,
                        "error": f"Missing required pattern: '{pattern}' - Agent won't handle varied inputs properly",
                    }

            # Check forbidden patterns
            for pattern in AGENT_VALIDATION_RULES["forbidden_patterns"]:
                if pattern in code:
                    return {
                        "valid": False,
                        "error": f"Forbidden pattern found: '{pattern}' - Agents must never crash",
                    }

            return {"valid": True}

        except SyntaxError as e:
            return {"valid": False, "error": f"Syntax error: {str(e)}"}

    def _extract_tags(self, description: str) -> List[str]:
        """Extract relevant tags from description."""

        tags = []

        # Keywords to look for
        keywords = {
            "pdf": ["pdf-processing", "document"],
            "excel": ["excel", "spreadsheet"],
            "csv": ["csv", "data-processing"],
            "chart": ["visualization", "plotting"],
            "email": ["communication", "extraction"],
            "statistic": ["statistics", "analysis"],
            "summary": ["summarization", "analysis"],
            "jira": ["ticketing", "project-management"],
            "slack": ["communication", "messaging"],
        }

        description_lower = description.lower()

        for keyword, tag_list in keywords.items():
            if keyword in description_lower:
                tags.extend(tag_list)

        # Remove duplicates and limit to 5 tags
        return list(set(tags))[:5]


class AgentFactoryCLI:
    """Command-line interface for testing agent creation."""

    def __init__(self):
        self.factory = AgentFactory()
        self.registry = RegistryManager()

    def run(self):
        """Run interactive agent creation."""

        print("\n" + "=" * 50)
        print("AGENT FACTORY - Interactive Agent Creation")
        print("=" * 50)

        # Get agent details from user
        print("\nEnter agent details:")
        agent_name = input("Agent name (e.g., pdf_summarizer): ").strip()
        description = input("Description: ").strip()

        # Show available tools
        print("\nAvailable tools:")
        tools = self.registry.list_tools()
        for tool in tools:
            print(f"  - {tool['name']}: {tool['description']}")

        print("\nEnter required tools (comma-separated):")
        tools_input = input("Tools: ").strip()
        required_tools = [t.strip() for t in tools_input.split(",") if t.strip()]

        input_desc = input("Input description: ").strip()
        output_desc = input("Output description: ").strip()

        # Optional workflow steps
        add_steps = input("\nAdd workflow steps? (y/n): ").lower() == "y"
        workflow_steps = []

        if add_steps:
            print("Enter workflow steps (type 'done' to finish):")
            while True:
                step = input(f"Step {len(workflow_steps) + 1}: ").strip()
                if step.lower() == "done":
                    break
                workflow_steps.append(step)

        print("\nGenerating agent code...")
        result = self.factory.create_agent(
            agent_name=agent_name,
            description=description,
            required_tools=required_tools,
            input_description=input_desc,
            output_description=output_desc,
            workflow_steps=workflow_steps if workflow_steps else None,
        )

        if result["status"] == "success":
            print(f"\nSuccess! Agent '{agent_name}' created")
            print(f"Location: generated/agents/{agent_name}_agent.py")
            print(f"Lines: {result['line_count']}")
            print("\nGenerated code preview (first 20 lines):")
            print("-" * 40)
            lines = result["code"].splitlines()[:20]
            for line in lines:
                print(line)
            if len(result["code"].splitlines()) > 20:
                print("... (truncated)")
            print("-" * 40)
        else:
            print(f"\nError: {result['message']}")
            if "missing_tools" in result:
                print(f"Missing tools: {', '.join(result['missing_tools'])}")
                print("Please create these tools first using the Tool Factory")


if __name__ == "__main__":
    cli = AgentFactoryCLI()
    cli.run()
