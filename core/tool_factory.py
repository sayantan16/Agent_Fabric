"""
Tool Factory
Dynamically generates tool code using Claude API
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
    CLAUDE_MODEL,
    CLAUDE_TEMPERATURE,
    MIN_TOOL_LINES,
    MAX_TOOL_LINES,
    ALLOWED_IMPORTS,
    EXAMPLE_TOOL_TEMPLATE,
)
from core.registry import RegistryManager


class ToolFactory:
    def __init__(self):
        self.client = Anthropic(api_key=ANTHROPIC_API_KEY)
        self.registry = RegistryManager()
        self.allowed_imports = ALLOWED_IMPORTS

    def create_tool(
        self,
        tool_name: str,
        description: str,
        input_description: str,
        output_description: str,
        examples: List[Dict] = None,
    ) -> Dict:
        """
        Create a new tool using Claude.

        Args:
            tool_name: Name of the tool function
            description: What the tool does
            input_description: Description of input parameters
            output_description: Description of output format
            examples: Optional input/output examples

        Returns:
            Dict with status and generated code or error
        """

        # Check if tool already exists
        if self.registry.tool_exists(tool_name):
            return {
                "status": "exists",
                "message": f"Tool '{tool_name}' already exists in registry",
            }

        # Build the prompt
        prompt = self._build_tool_prompt(
            tool_name, description, input_description, output_description, examples
        )

        try:
            # Call Claude API
            response = self.client.messages.create(
                model=CLAUDE_MODEL,
                temperature=CLAUDE_TEMPERATURE,
                max_tokens=1000,
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
            validation_result = self._validate_tool_code(code, tool_name)

            if validation_result["valid"]:
                # Register the tool
                self.registry.register_tool(
                    name=tool_name,
                    description=description,
                    code=code,
                    tags=self._extract_tags(description),
                )

                return {
                    "status": "success",
                    "code": code,
                    "message": f"Tool '{tool_name}' created successfully",
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

    def _build_tool_prompt(
        self,
        tool_name: str,
        description: str,
        input_desc: str,
        output_desc: str,
        examples: List[Dict],
    ) -> str:
        """Build the prompt for Claude to generate tool code."""

        prompt = f"""Generate a Python function that follows these specifications:

FUNCTION NAME: {tool_name}

DESCRIPTION: {description}

INPUT: {input_desc}

OUTPUT: {output_desc}

REQUIREMENTS:
1. Must be a PURE function (no side effects, no file I/O, no API calls)
2. Must be between {MIN_TOOL_LINES} and {MAX_TOOL_LINES} lines
3. All imports must be inside the function
4. Must handle edge cases gracefully
5. Must return consistent data types
6. Can only use these allowed imports: {', '.join(self.allowed_imports)}

EXAMPLE STRUCTURE TO FOLLOW:
{EXAMPLE_TOOL_TEMPLATE}

"""

        if examples:
            prompt += "\nEXAMPLES:\n"
            for i, example in enumerate(examples, 1):
                prompt += f"Example {i}:\n"
                prompt += f"  Input: {example.get('input')}\n"
                prompt += f"  Output: {example.get('output')}\n"

        prompt += """
OUTPUT ONLY THE PYTHON CODE. Do not include any explanation or markdown formatting.
The code should start with 'def' and be valid Python.
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

    def _validate_tool_code(self, code: str, expected_name: str) -> Dict:
        """Validate the generated tool code."""

        try:
            # Parse the code to check syntax
            tree = ast.parse(code)

            # Check if it's a function definition
            if not isinstance(tree.body[0], ast.FunctionDef):
                return {"valid": False, "error": "Code is not a function definition"}

            # Check function name
            func_name = tree.body[0].name
            if func_name != expected_name:
                return {
                    "valid": False,
                    "error": f"Function name '{func_name}' doesn't match expected '{expected_name}'",
                }

            # Check line count
            line_count = len(code.splitlines())
            if line_count < MIN_TOOL_LINES:
                return {
                    "valid": False,
                    "error": f"Code too short: {line_count} lines (minimum: {MIN_TOOL_LINES})",
                }
            if line_count > MAX_TOOL_LINES:
                return {
                    "valid": False,
                    "error": f"Code too long: {line_count} lines (maximum: {MAX_TOOL_LINES})",
                }

            # Check for forbidden operations
            for node in ast.walk(tree):
                # Check for file I/O
                if isinstance(node, ast.Name) and node.id in ["open", "file"]:
                    return {
                        "valid": False,
                        "error": "Code contains file I/O operations",
                    }

                # Check for network operations
                if isinstance(node, ast.Name) and node.id in [
                    "requests",
                    "urllib",
                    "socket",
                ]:
                    return {"valid": False, "error": "Code contains network operations"}

            return {"valid": True}

        except SyntaxError as e:
            return {"valid": False, "error": f"Syntax error: {str(e)}"}
        except Exception as e:
            return {"valid": False, "error": f"Validation error: {str(e)}"}

    def _extract_tags(self, description: str) -> List[str]:
        """Extract relevant tags from description."""

        tags = []

        # Keywords to look for
        keywords = {
            "extract": ["extraction", "parsing"],
            "calculate": ["calculation", "math"],
            "convert": ["conversion", "transformation"],
            "validate": ["validation", "checking"],
            "format": ["formatting", "display"],
            "analyze": ["analysis", "processing"],
            "text": ["text-processing"],
            "number": ["numeric", "math"],
            "date": ["datetime", "temporal"],
            "url": ["web", "link"],
            "email": ["communication"],
            "json": ["data", "structured"],
            "csv": ["data", "tabular"],
        }

        description_lower = description.lower()

        for keyword, tag_list in keywords.items():
            if keyword in description_lower:
                tags.extend(tag_list)

        # Remove duplicates and limit to 5 tags
        return list(set(tags))[:5]


class ToolFactoryCLI:
    """Command-line interface for testing tool creation."""

    def __init__(self):
        self.factory = ToolFactory()

    def run(self):
        """Run interactive tool creation."""

        print("\n" + "=" * 50)
        print("TOOL FACTORY - Interactive Tool Creation")
        print("=" * 50)

        # Get tool details from user
        print("\nEnter tool details:")
        tool_name = input("Tool name (e.g., extract_urls): ").strip()
        description = input("Description: ").strip()
        input_desc = input("Input description: ").strip()
        output_desc = input("Output description: ").strip()

        # Optional examples
        add_examples = input("\nAdd examples? (y/n): ").lower() == "y"
        examples = []

        if add_examples:
            while True:
                example_input = input("Example input (or 'done'): ").strip()
                if example_input.lower() == "done":
                    break
                example_output = input("Expected output: ").strip()
                examples.append({"input": example_input, "output": example_output})

        print("\nGenerating tool code...")
        result = self.factory.create_tool(
            tool_name=tool_name,
            description=description,
            input_description=input_desc,
            output_description=output_desc,
            examples=examples if examples else None,
        )

        if result["status"] == "success":
            print(f"\nSuccess! Tool '{tool_name}' created")
            print(f"Location: generated/tools/{tool_name}.py")
            print(f"Lines: {result['line_count']}")
            print("\nGenerated code:")
            print("-" * 40)
            print(result["code"])
            print("-" * 40)
        else:
            print(f"\nError: {result['message']}")
            if "code" in result:
                print("\nGenerated code (with errors):")
                print("-" * 40)
                print(result["code"])
                print("-" * 40)


if __name__ == "__main__":
    cli = ToolFactoryCLI()
    cli.run()
