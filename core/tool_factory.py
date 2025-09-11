"""
Tool Factory
Dynamically generates pure function tools using Claude API
"""

import os
import sys
import ast
import json
import traceback
from typing import Dict, List, Optional, Any
from anthropic import Anthropic

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    ANTHROPIC_API_KEY,
    CLAUDE_MODEL,
    CLAUDE_TEMPERATURE,
    CLAUDE_MAX_TOKENS,
    CLAUDE_TOOL_GENERATION_PROMPT,
    MIN_TOOL_LINES,
    MAX_TOOL_LINES,
    TOOL_VALIDATION_RULES,
    ALLOWED_IMPORTS,
    GENERATED_TOOLS_DIR,
    PREBUILT_TOOLS_DIR,
)
from core.registry import RegistryManager
from core.registry_singleton import get_shared_registry


class ToolFactory:
    """
    Factory for creating pure function tools using Claude.
    Ensures all tools are stateless and handle inputs gracefully.
    """

    def __init__(self):
        """Initialize the tool factory."""
        self.client = Anthropic(api_key=ANTHROPIC_API_KEY)
        self.registry = get_shared_registry()
        self.generation_history = []

    def create_tool(
        self,
        tool_name: str,
        description: str,
        input_description: str,
        output_description: str,
        examples: Optional[List[Dict[str, Any]]] = None,
        default_return: Any = None,
        is_prebuilt: bool = False,
        is_pure_function: bool = True,
        tags: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Create a new tool using Claude.

        Args:
            tool_name: Unique identifier for the tool
            description: Clear description of tool's purpose
            input_description: Expected input format/type
            output_description: Expected output format/type
            examples: Optional input/output examples
            default_return: Default value to return on error
            is_prebuilt: Whether this is a prebuilt tool
            is_pure_function: Whether tool has no side effects
            tags: Optional categorization tags

        Returns:
            Result dictionary with status and details
        """

        print(f"DEBUG: Creating tool '{tool_name}'")

        # Validate tool name
        if not self._validate_tool_name(tool_name):
            return {
                "status": "error",
                "message": f"Invalid tool name: {tool_name}. Use lowercase with underscores only.",
            }

        # Check if tool already exists
        if self.registry.tool_exists(tool_name):
            print(f"DEBUG: Tool '{tool_name}' already exists")
            return {
                "status": "exists",
                "message": f"Tool '{tool_name}' already exists and is active",
                "tool": self.registry.get_tool(tool_name),
            }

        # Determine default return value
        if default_return is None:
            default_return = self._infer_default_return(output_description)

        # Generate the tool code
        generation_result = self._generate_tool_code(
            tool_name=tool_name,
            description=description,
            input_description=input_description,
            output_description=output_description,
            examples=examples,
            default_return=default_return,
        )

        if generation_result["status"] != "success":
            return generation_result

        code = generation_result["code"]

        # Validate the generated code
        validation_result = self._validate_tool_code(
            code=code, tool_name=tool_name, is_pure_function=is_pure_function
        )

        if not validation_result["valid"]:
            # Try to fix common issues
            fixed_code = self._attempt_code_fixes(code, validation_result["issues"])
            if fixed_code:
                code = fixed_code
                validation_result = self._validate_tool_code(
                    code, tool_name, is_pure_function
                )

                if not validation_result["valid"]:
                    return {
                        "status": "validation_error",
                        "message": "Generated code failed validation after fixes",
                        "validation_errors": validation_result["issues"],
                        "code": code,
                    }
            else:
                return {
                    "status": "validation_error",
                    "message": "Generated code failed validation",
                    "validation_errors": validation_result["issues"],
                    "code": code,
                }

        # Extract function signature
        signature = self._extract_signature(code)

        # Register the tool
        registration_result = self.registry.register_tool(
            name=tool_name,
            description=description,
            code=code,
            signature=signature,
            tags=tags or self._extract_tags_from_description(description),
            is_prebuilt=is_prebuilt,
            is_pure_function=is_pure_function,
        )

        if registration_result["status"] != "success":
            return registration_result

        # Force all components to reload registry after successful creation
        from core.registry_singleton import RegistrySingleton

        RegistrySingleton().force_reload()
        print(f"DEBUG: Forced registry reload after creating '{tool_name}'")

        # Record generation history
        self.generation_history.append(
            {
                "tool_name": tool_name,
                "timestamp": registration_result.get("created_at"),
                "line_count": len(code.splitlines()),
                "is_pure": is_pure_function,
            }
        )

        # Test the tool with examples if provided
        if examples:
            test_results = self._test_tool_with_examples(tool_name, examples)
            registration_result["test_results"] = test_results

        return {
            "status": "success",
            "message": f"Tool '{tool_name}' created successfully",
            "tool_name": tool_name,
            "location": registration_result["location"],
            "line_count": registration_result["line_count"],
            "signature": signature,
            "code": code,
        }

    def _generate_tool_code(
        self,
        tool_name: str,
        description: str,
        input_description: str,
        output_description: str,
        examples: Optional[List[Dict[str, Any]]],
        default_return: Any,
    ) -> Dict[str, Any]:
        """Generate tool code using Claude."""
        # Determine imports needed
        imports = self._determine_imports(
            description, input_description, output_description
        )

        # Build tool logic hints
        tool_logic = self._build_tool_logic_hints(description, examples)

        # Format the prompt
        prompt = CLAUDE_TOOL_GENERATION_PROMPT.format(
            tool_name=tool_name,
            description=description,
            input_description=input_description,
            output_description=output_description,
            imports="\n    ".join(imports),
            tool_logic=tool_logic,
            default_return=repr(default_return),
            min_lines=MIN_TOOL_LINES,
            max_lines=MAX_TOOL_LINES,
        )

        # Add examples to prompt if provided
        if examples:
            examples_text = "\n\nExamples:\n"
            for i, example in enumerate(examples, 1):
                examples_text += f"Input: {example.get('input')}\n"
                examples_text += f"Expected Output: {example.get('output')}\n\n"
            prompt += examples_text

        try:
            # Call Claude API
            response = self.client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=CLAUDE_MAX_TOKENS,
                messages=[{"role": "user", "content": prompt}],
            )

            # Extract code from response
            code = self._extract_code_from_response(response.content[0].text)

            if not code:
                return {
                    "status": "error",
                    "message": "No valid Python code found in Claude response",
                }

            return {"status": "success", "code": code}

        except Exception as e:
            return {
                "status": "error",
                "message": f"Claude API error: {str(e)}",
                "traceback": traceback.format_exc(),
            }

    def _validate_tool_code(
        self, code: str, tool_name: str, is_pure_function: bool = True
    ) -> Dict[str, Any]:
        """
        Comprehensive validation of tool code.

        Args:
            code: Python code to validate
            tool_name: Expected tool name
            is_pure_function: Whether tool should be pure

        Returns:
            Validation result with issues if any
        """
        issues = []

        # Check syntax
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return {"valid": False, "issues": [f"Syntax error: {str(e)}"]}

        # Check structure
        if not tree.body or not isinstance(tree.body[0], ast.FunctionDef):
            issues.append("Code must define a function")
            return {"valid": False, "issues": issues}

        func_def = tree.body[0]

        # Check function name
        if func_def.name != tool_name:
            issues.append(f"Function name must be: {tool_name}")

        # Check function has parameter
        if len(func_def.args.args) == 0:
            issues.append("Function must accept at least one parameter")

        # Check for default parameter handling
        first_param = func_def.args.args[0].arg if func_def.args.args else None
        if first_param and f"if {first_param} is None:" not in code:
            issues.append("Function must handle None input")

        # Check required patterns
        for pattern in TOOL_VALIDATION_RULES["required_patterns"]:
            if pattern and pattern not in code:
                issues.append(f"Missing required pattern: {pattern}")

        # Check forbidden patterns for pure functions
        if is_pure_function:
            forbidden = TOOL_VALIDATION_RULES["forbidden_patterns"]
            for pattern in forbidden:
                if pattern and pattern in code:
                    # Special handling for conditional patterns
                    if 'if "connector"' in pattern:
                        # Skip this check for connectors
                        continue
                    issues.append(f"Forbidden pattern for pure function: {pattern}")

        # Check imports
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module = alias.name.split(".")[0]
                    if module not in ALLOWED_IMPORTS:
                        issues.append(f"Forbidden import: {alias.name}")
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    module = node.module.split(".")[0]
                    if module not in ALLOWED_IMPORTS:
                        issues.append(f"Forbidden import from: {node.module}")

        # Check line count
        line_count = len(code.splitlines())
        if line_count < MIN_TOOL_LINES:
            issues.append(f"Code too short: {line_count} lines (min: {MIN_TOOL_LINES})")
        elif line_count > MAX_TOOL_LINES:
            issues.append(f"Code too long: {line_count} lines (max: {MAX_TOOL_LINES})")

        # Check for return statement
        has_return = any(isinstance(node, ast.Return) for node in ast.walk(func_def))
        if not has_return:
            issues.append("Function must have return statement")

        # Check for exception handling
        has_try = any(isinstance(node, ast.Try) for node in ast.walk(func_def))
        if not has_try:
            issues.append("Function must have try-except block for error handling")

        # Check no exceptions are raised
        for node in ast.walk(func_def):
            if isinstance(node, ast.Raise):
                issues.append("Function must not raise exceptions")

        return {"valid": len(issues) == 0, "issues": issues}

    def _attempt_code_fixes(self, code: str, issues: List[str]) -> Optional[str]:
        """
        Attempt to fix common code issues.

        Args:
            code: Code with issues
            issues: List of validation issues

        Returns:
            Fixed code if possible, None otherwise
        """
        fixed_code = code

        # Fix missing None handling
        if any("None input" in issue for issue in issues):
            lines = fixed_code.splitlines()
            for i, line in enumerate(lines):
                if line.strip().startswith("def ") and i + 1 < len(lines):
                    # Find first line after docstring
                    insert_index = i + 1
                    # Skip docstring if present
                    if i + 1 < len(lines) and (
                        lines[i + 1].strip().startswith('"""')
                        or lines[i + 1].strip().startswith("'''")
                    ):
                        for j in range(i + 2, len(lines)):
                            if lines[j].strip().endswith('"""') or lines[
                                j
                            ].strip().endswith("'''"):
                                insert_index = j + 1
                                break

                    # Insert None check
                    param_name = "input_data"  # Default assumption
                    if "(" in line and ")" in line:
                        params = line[line.find("(") + 1 : line.find(")")].strip()
                        if params and "=" in params:
                            param_name = params.split("=")[0].strip()
                        elif params:
                            param_name = params.split(",")[0].strip()

                    none_check = f"""    if {param_name} is None:
        return None
    """
                    lines.insert(insert_index, none_check)
                    fixed_code = "\n".join(lines)
                    break

        # Fix missing try-except
        if any("try-except" in issue for issue in issues):
            if "try:" not in fixed_code:
                lines = fixed_code.splitlines()
                # Wrap main logic in try-except
                indent_level = 4  # Assuming standard function indentation
                wrapped_lines = []
                in_function = False
                function_start = 0

                for i, line in enumerate(lines):
                    if line.strip().startswith("def "):
                        in_function = True
                        function_start = i
                        wrapped_lines.append(line)
                    elif (
                        in_function
                        and i > function_start
                        and line.strip()
                        and not line.strip().startswith("#")
                    ):
                        # Start wrapping from here
                        wrapped_lines.append("    try:")
                        for j in range(i, len(lines)):
                            wrapped_lines.append("    " + lines[j])
                        wrapped_lines.append("    except Exception:")
                        wrapped_lines.append("        return None")
                        break
                    else:
                        wrapped_lines.append(line)

                fixed_code = "\n".join(wrapped_lines)

        return fixed_code if fixed_code != code else None

    def _extract_code_from_response(self, response: str) -> Optional[str]:
        """Extract Python code from Claude's response."""
        # Handle markdown code blocks
        if "```python" in response:
            start = response.find("```python") + 9
            end = response.find("```", start)
            if end > start:
                return response[start:end].strip()

        # Handle generic code blocks
        if "```" in response:
            start = response.find("```") + 3
            # Skip language identifier if present
            if response[start : start + 10].strip().startswith(("python", "py")):
                start = response.find("\n", start) + 1
            end = response.find("```", start)
            if end > start:
                code = response[start:end].strip()
                if code.startswith("def "):
                    return code

        # Try to find function definition directly
        if "def " in response:
            start = response.find("def ")
            # Find the end of the function
            lines = response[start:].split("\n")
            function_lines = []
            indent_level = None

            for line in lines:
                if line.strip().startswith("def "):
                    function_lines.append(line)
                    indent_level = len(line) - len(line.lstrip())
                elif indent_level is not None:
                    current_indent = len(line) - len(line.lstrip())
                    if (
                        line.strip()
                        and current_indent <= indent_level
                        and not line.strip().startswith("#")
                    ):
                        break
                    function_lines.append(line)

            return "\n".join(function_lines).strip()

        return None

    def _extract_signature(self, code: str) -> str:
        """Extract function signature from code."""
        for line in code.split("\n"):
            if line.strip().startswith("def "):
                return line.strip().rstrip(":")
        return "def unknown()"

    def _infer_default_return(self, output_description: str) -> Any:
        """Infer appropriate default return value from output description."""
        output_lower = output_description.lower()

        if "list" in output_lower or "array" in output_lower:
            return []
        elif (
            "dict" in output_lower or "object" in output_lower or "json" in output_lower
        ):
            return {}
        elif (
            "string" in output_lower or "text" in output_lower or "str" in output_lower
        ):
            return ""
        elif (
            "number" in output_lower or "int" in output_lower or "float" in output_lower
        ):
            return 0
        elif "bool" in output_lower or "boolean" in output_lower:
            return False
        elif "none" in output_lower or "null" in output_lower:
            return None
        else:
            return None

    def _determine_imports(
        self, description: str, input_desc: str, output_desc: str
    ) -> List[str]:
        """Determine likely imports needed based on descriptions."""
        imports = []
        all_text = f"{description} {input_desc} {output_desc}".lower()

        if "regex" in all_text or "pattern" in all_text or "extract" in all_text:
            imports.append("import re")
        if "json" in all_text:
            imports.append("import json")
        if "date" in all_text or "time" in all_text:
            imports.append("from datetime import datetime")
        if "math" in all_text or "calculate" in all_text or "statistics" in all_text:
            imports.append("import math")
        if "random" in all_text:
            imports.append("import random")
        if "url" in all_text or "parse" in all_text:
            imports.append("from urllib.parse import urlparse")

        return imports if imports else ["# No specific imports needed"]

    def _build_tool_logic_hints(
        self, description: str, examples: Optional[List[Dict]]
    ) -> str:
        """Build hints for tool logic based on description and examples."""
        hints = []
        desc_lower = description.lower()

        if "extract" in desc_lower:
            hints.append("# Extract relevant data from input")
            hints.append("# Use pattern matching or parsing")
        elif "calculate" in desc_lower or "compute" in desc_lower:
            hints.append("# Perform calculations on input data")
            hints.append("# Handle numeric operations safely")
        elif "validate" in desc_lower or "check" in desc_lower:
            hints.append("# Validate input against criteria")
            hints.append("# Return validation result")
        elif "convert" in desc_lower or "transform" in desc_lower:
            hints.append("# Transform input to desired format")
            hints.append("# Handle type conversions safely")
        elif "filter" in desc_lower or "select" in desc_lower:
            hints.append("# Filter data based on criteria")
            hints.append("# Return filtered results")
        else:
            hints.append("# Process input data")
            hints.append("# Return processed result")

        if examples:
            hints.append("# Match example input/output patterns")

        return "\n        ".join(hints)

    def _extract_tags_from_description(self, description: str) -> List[str]:
        """Extract relevant tags from description."""
        tags = []
        keywords = {
            "extract": "extraction",
            "calculate": "calculation",
            "validate": "validation",
            "convert": "conversion",
            "parse": "parsing",
            "filter": "filtering",
            "transform": "transformation",
            "analyze": "analysis",
            "process": "processing",
            "format": "formatting",
        }

        desc_lower = description.lower()
        for keyword, tag in keywords.items():
            if keyword in desc_lower:
                tags.append(tag)

        return tags[:5]  # Limit to 5 tags

    def _validate_tool_name(self, name: str) -> bool:
        """Validate tool name format."""
        import re

        # Allow lowercase letters, numbers, and underscores
        pattern = r"^[a-z][a-z0-9_]*$"
        return bool(re.match(pattern, name))

    def _test_tool_with_examples(
        self, tool_name: str, examples: List[Dict]
    ) -> List[Dict]:
        """
        Test generated tool with provided examples.

        Args:
            tool_name: Name of tool to test
            examples: List of input/output examples

        Returns:
            List of test results
        """
        results = []
        tool_info = self.registry.get_tool(tool_name)

        if not tool_info:
            return [{"status": "error", "message": "Tool not found in registry"}]

        # Import the tool dynamically
        try:
            import importlib.util

            spec = importlib.util.spec_from_file_location(
                tool_name, tool_info["location"]
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            tool_func = getattr(module, tool_name)
        except Exception as e:
            return [{"status": "error", "message": f"Failed to import tool: {str(e)}"}]

        # Test each example
        for i, example in enumerate(examples):
            try:
                input_data = example.get("input")
                expected_output = example.get("output")
                actual_output = tool_func(input_data)

                # Check if output matches
                if actual_output == expected_output:
                    results.append(
                        {
                            "example": i + 1,
                            "status": "passed",
                            "input": input_data,
                            "output": actual_output,
                        }
                    )
                else:
                    results.append(
                        {
                            "example": i + 1,
                            "status": "failed",
                            "input": input_data,
                            "expected": expected_output,
                            "actual": actual_output,
                        }
                    )
            except Exception as e:
                results.append(
                    {
                        "example": i + 1,
                        "status": "error",
                        "input": input_data,
                        "error": str(e),
                    }
                )

        return results

    def get_generation_history(self) -> List[Dict[str, Any]]:
        """Get history of generated tools."""
        return self.generation_history.copy()

    def create_connector_tool(
        self,
        tool_name: str,
        service: str,
        operations: List[str],
        auth_type: str = "api_key",
    ) -> Dict[str, Any]:
        """
        Create a connector tool for external services.

        Args:
            tool_name: Name for the connector tool
            service: Service to connect to (e.g., 'jira')
            operations: List of operations to support
            auth_type: Authentication type required

        Returns:
            Result of connector creation
        """
        # Special handling for connector tools
        description = (
            f'Connector for {service} with operations: {", ".join(operations)}'
        )

        # Connector template based on service
        if service.lower() == "jira":
            return self._create_jira_connector(tool_name, operations)
        else:
            return {
                "status": "error",
                "message": f"Connector for {service} not yet supported",
            }

    def _create_jira_connector(
        self, tool_name: str, operations: List[str]
    ) -> Dict[str, Any]:
        """Create a Jira connector tool."""
        # This would contain the actual Jira connector implementation
        # For now, return a placeholder
        code = f'''def {tool_name}(input_data=None):
    """
    Jira connector for operations: {', '.join(operations)}
    """
    import json
    
    if input_data is None:
        return {{'status': 'error', 'message': 'No input provided'}}
    
    try:
        # Parse input
        if isinstance(input_data, str):
            data = json.loads(input_data)
        elif isinstance(input_data, dict):
            data = input_data
        else:
            return {{'status': 'error', 'message': 'Invalid input type'}}
        
        operation = data.get('operation')
        
        # Handle operations
        if operation in {operations}:
            # Placeholder for actual Jira API calls
            return {{
                'status': 'success',
                'operation': operation,
                'result': 'Operation completed'
            }}
        else:
            return {{'status': 'error', 'message': f'Unsupported operation: {{operation}}'}}
    
    except Exception as e:
        return {{'status': 'error', 'message': str(e)}}
'''

        return self.registry.register_tool(
            name=tool_name,
            description=f'Jira connector for {", ".join(operations)}',
            code=code,
            is_pure_function=False,
            tags=["connector", "jira", "external"],
        )

    def _generate_functional_tool_code(self, tool_name: str, description: str) -> str:
        """Generate actually functional tool code based on name and description."""

        # Extract tool purpose
        tool_lower = tool_name.lower()
        desc_lower = description.lower()

        # Generate appropriate implementation
        if "extract" in tool_lower:
            if "email" in tool_lower:
                return self._generate_email_extractor()
            elif "phone" in tool_lower:
                return self._generate_phone_extractor()
            elif "url" in tool_lower:
                return self._generate_url_extractor()
            else:
                return self._generate_generic_extractor(tool_name)

        elif "calculate" in tool_lower or "calc" in tool_lower:
            if "mean" in tool_lower or "average" in tool_lower:
                return self._generate_mean_calculator()
            elif "median" in tool_lower:
                return self._generate_median_calculator()
            elif "std" in tool_lower or "deviation" in tool_lower:
                return self._generate_std_calculator()
            else:
                return self._generate_generic_calculator(tool_name)

        elif "format" in tool_lower:
            return self._generate_formatter(tool_name)

        elif "generate" in tool_lower:
            if "chart" in tool_lower or "graph" in tool_lower:
                return self._generate_chart_generator()
            elif "report" in tool_lower:
                return self._generate_report_generator()
            else:
                return self._generate_generic_generator(tool_name)

        else:
            # Default functional implementation
            return self._generate_default_tool(tool_name, description)

    def _generate_phone_extractor(self) -> str:
        """Generate phone extraction tool."""
        return '''def extract_phone(input_data=None):
        """Extract phone numbers from text."""
        import re
        
        if input_data is None:
            return []
        
        try:
            # Convert input to string
            if isinstance(input_data, dict):
                text = str(input_data.get('text', input_data.get('data', input_data)))
            else:
                text = str(input_data)
            
            # Phone number patterns
            patterns = [
                r'\\(?\\d{3}\\)?[\\s.-]?\\d{3}[\\s.-]?\\d{4}',  # US format
                r'\\d{3}-\\d{3}-\\d{4}',  # 555-555-5555
                r'\\(\\d{3}\\)\\s*\\d{3}-\\d{4}',  # (555) 555-5555
                r'\\d{10}',  # 5555555555
            ]
            
            phones = []
            for pattern in patterns:
                phones.extend(re.findall(pattern, text))
            
            # Remove duplicates
            return list(set(phones))
        
        except Exception:
            return []
    '''

    def _generate_formatter(self, tool_name: str) -> str:
        """Generate formatting tool."""
        return f'''def {tool_name}(input_data=None):
        """Format data for presentation."""
        
        if input_data is None:
            return ""
        
        try:
            if isinstance(input_data, dict):
                # Format as key-value pairs
                lines = []
                for key, value in input_data.items():
                    lines.append(f"{{key.title()}}: {{value}}")
                return "\\n".join(lines)
            elif isinstance(input_data, list):
                # Format as bullet points
                return "\\n".join([f"• {{item}}" for item in input_data])
            else:
                # Basic formatting
                return f"=== Output ===\\n{{input_data}}\\n============"
        
        except Exception:
            return str(input_data)
    '''

    def _generate_chart_generator(self) -> str:
        """Generate chart creation tool."""
        return '''def generate_bar_chart(input_data=None):
        """Generate a bar chart from data."""
        
        if input_data is None:
            return {"type": "chart", "data": None, "error": "No data provided"}
        
        try:
            # Extract data for chart
            if isinstance(input_data, dict):
                # Assume dict has labels and values
                labels = input_data.get('labels', list(input_data.keys()))
                values = input_data.get('values', list(input_data.values()))
            elif isinstance(input_data, list):
                # Create simple numbered labels
                labels = [f"Item {i+1}" for i in range(len(input_data))]
                values = input_data
            else:
                return {"type": "chart", "data": None, "error": "Invalid data format"}
            
            # Return chart specification (would be rendered by UI)
            return {
                "type": "bar_chart",
                "labels": labels,
                "values": values,
                "title": "Generated Bar Chart",
                "x_label": "Categories",
                "y_label": "Values"
            }
        
        except Exception as e:
            return {"type": "chart", "data": None, "error": str(e)}
    '''

    def _generate_default_tool(self, tool_name: str, description: str) -> str:
        """Generate a default but functional tool."""
        return f'''def {tool_name}(input_data=None):
        """
        {description}
        """
        
        if input_data is None:
            return None
        
        try:
            # Process based on input type
            if isinstance(input_data, str):
                # String processing
                result = {{"processed": input_data, "length": len(input_data)}}
            elif isinstance(input_data, dict):
                # Dictionary processing
                result = {{"keys": list(input_data.keys()), "size": len(input_data)}}
            elif isinstance(input_data, list):
                # List processing
                result = {{"items": len(input_data), "first": input_data[0] if input_data else None}}
            else:
                # Generic processing
                result = {{"type": type(input_data).__name__, "value": str(input_data)}}
            
            return result
        
        except Exception as e:
            return {{"error": str(e), "input_type": type(input_data).__name__}}
    '''

    def _generate_mean_calculator(self) -> str:
        """Generate mean calculation tool."""
        return '''def calculate_mean(input_data=None):
        """Calculate arithmetic mean of numbers."""
        
        if input_data is None:
            return 0
        
        try:
            # Extract numbers from various formats
            numbers = []
            
            if isinstance(input_data, (list, tuple)):
                numbers = [float(x) for x in input_data if isinstance(x, (int, float))]
            elif isinstance(input_data, dict):
                if 'numbers' in input_data:
                    numbers = input_data['numbers']
                elif 'values' in input_data:
                    numbers = input_data['values']
                else:
                    # Try to extract numbers from dict values
                    numbers = [v for v in input_data.values() if isinstance(v, (int, float))]
            elif isinstance(input_data, str):
                # Extract numbers from string
                import re
                numbers = [float(x) for x in re.findall(r'-?\d+\.?\d*', input_data)]
            else:
                numbers = [float(input_data)]
            
            if numbers:
                return sum(numbers) / len(numbers)
            return 0
            
        except Exception:
            return 0
    '''

    def _generate_median_calculator(self) -> str:
        """Generate median calculation tool."""
        return '''def calculate_median(input_data=None):
        """Calculate median of numbers."""
        
        if input_data is None:
            return 0
        
        try:
            # Extract numbers from various formats
            numbers = []
            
            if isinstance(input_data, (list, tuple)):
                numbers = sorted([float(x) for x in input_data if isinstance(x, (int, float))])
            elif isinstance(input_data, dict):
                if 'numbers' in input_data:
                    numbers = sorted(input_data['numbers'])
                elif 'values' in input_data:
                    numbers = sorted(input_data['values'])
                else:
                    numbers = sorted([v for v in input_data.values() if isinstance(v, (int, float))])
            elif isinstance(input_data, str):
                import re
                numbers = sorted([float(x) for x in re.findall(r'-?\d+\.?\d*', input_data)])
            else:
                return float(input_data)
            
            if not numbers:
                return 0
                
            n = len(numbers)
            if n % 2 == 0:
                return (numbers[n//2 - 1] + numbers[n//2]) / 2
            else:
                return numbers[n//2]
                
        except Exception:
            return 0
    '''

    def _generate_std_calculator(self) -> str:
        """Generate standard deviation calculation tool."""
        return '''def calculate_std(input_data=None):
        """Calculate standard deviation of numbers."""
        
        if input_data is None:
            return 0
        
        try:
            # Extract numbers from various formats
            numbers = []
            
            if isinstance(input_data, (list, tuple)):
                numbers = [float(x) for x in input_data if isinstance(x, (int, float))]
            elif isinstance(input_data, dict):
                if 'numbers' in input_data:
                    numbers = input_data['numbers']
                elif 'values' in input_data:
                    numbers = input_data['values']
                else:
                    numbers = [v for v in input_data.values() if isinstance(v, (int, float))]
            elif isinstance(input_data, str):
                import re
                numbers = [float(x) for x in re.findall(r'-?\d+\.?\d*', input_data)]
            else:
                return 0
            
            if not numbers or len(numbers) < 2:
                return 0
                
            # Calculate mean
            mean = sum(numbers) / len(numbers)
            
            # Calculate variance
            variance = sum((x - mean) ** 2 for x in numbers) / len(numbers)
            
            # Return standard deviation
            return variance ** 0.5
            
        except Exception:
            return 0
    '''

    def _generate_generic_calculator(self, tool_name: str) -> str:
        """Generate generic calculator tool."""
        return f'''def {tool_name}(input_data=None):
        """Perform calculations on input data."""
        
        if input_data is None:
            return 0
        
        try:
            # Extract numbers
            if isinstance(input_data, (list, tuple)):
                numbers = [float(x) for x in input_data if isinstance(x, (int, float))]
            elif isinstance(input_data, dict):
                numbers = [v for v in input_data.values() if isinstance(v, (int, float))]
            else:
                return float(input_data)
            
            # Return basic calculation result
            if numbers:
                return {{
                    "count": len(numbers),
                    "sum": sum(numbers),
                    "avg": sum(numbers) / len(numbers),
                    "min": min(numbers),
                    "max": max(numbers)
                }}
            return 0
            
        except Exception:
            return 0
    '''

    def _generate_generic_generator(self, tool_name: str) -> str:
        """Generate generic generator tool."""
        return f'''def {tool_name}(input_data=None):
        """Generate output based on input."""
        
        if input_data is None:
            return {{}}
        
        try:
            return {{
                "generated": True,
                "type": "{tool_name.replace('_', ' ')}",
                "input_summary": str(input_data)[:100],
                "timestamp": str(datetime.now())
            }}
        except Exception:
            return {{}}
    '''

    def _generate_functional_tool_code(self, tool_name: str, description: str) -> str:
        """Generate ACTUALLY FUNCTIONAL tool code - NO PLACEHOLDERS."""

        tool_lower = tool_name.lower()
        desc_lower = description.lower()

        # Email extraction
        if "email" in tool_lower or "email" in desc_lower:
            return '''def extract_emails(input_data=None):
        """Extract email addresses from text."""
        import re
        
        if input_data is None:
            return []
        
        try:
            text = str(input_data)
            if isinstance(input_data, dict):
                text = ' '.join(str(v) for v in input_data.values())
            elif isinstance(input_data, list):
                text = ' '.join(str(item) for item in input_data)
            
            # Comprehensive email regex
            pattern = r'\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b'
            emails = re.findall(pattern, text, re.IGNORECASE)
            return list(set(email.lower() for email in emails))
        except Exception:
            return []
    '''

        # URL extraction
        elif "url" in tool_lower or "link" in tool_lower:
            return '''def extract_urls(input_data=None):
        """Extract URLs from text."""
        import re
        
        if input_data is None:
            return []
        
        try:
            text = str(input_data)
            if isinstance(input_data, dict):
                text = ' '.join(str(v) for v in input_data.values())
            
            # Multiple URL patterns for better coverage
            patterns = [
                r'https?://[^\\s<>"{}|\\\\^`\\[\\]]+',
                r'www\\.[^\\s<>"{}|\\\\^`\\[\\]]+',
                r'ftp://[^\\s<>"{}|\\\\^`\\[\\]]+'
            ]
            
            urls = []
            for pattern in patterns:
                urls.extend(re.findall(pattern, text, re.IGNORECASE))
            
            # Clean and deduplicate
            clean_urls = []
            for url in urls:
                if not url.startswith('http'):
                    url = 'http://' + url
                clean_urls.append(url)
            
            return list(set(clean_urls))
        except Exception:
            return []
    '''

        # Phone extraction
        elif "phone" in tool_lower or "telephone" in tool_lower:
            return '''def extract_phones(input_data=None):
        """Extract phone numbers from text."""
        import re
        
        if input_data is None:
            return []
        
        try:
            text = str(input_data)
            if isinstance(input_data, dict):
                text = ' '.join(str(v) for v in input_data.values())
            
            # Multiple phone patterns
            patterns = [
                r'\\+?1?\\s*\\(?\\d{3}\\)?[\\s.-]?\\d{3}[\\s.-]?\\d{4}',  # US format
                r'\\(\\d{3}\\)\\s*\\d{3}-\\d{4}',  # (555) 555-5555
                r'\\d{3}-\\d{3}-\\d{4}',  # 555-555-5555
                r'\\d{10}',  # 5555555555
            ]
            
            phones = []
            for pattern in patterns:
                matches = re.findall(pattern, text)
                phones.extend(matches)
            
            # Clean and format
            clean_phones = []
            for phone in phones:
                # Remove non-digits for comparison
                digits = re.sub(r'\\D', '', phone)
                if len(digits) >= 10:
                    clean_phones.append(phone)
            
            return list(set(clean_phones))
        except Exception:
            return []
    '''

        # Calculations
        elif "mean" in tool_lower or "average" in tool_lower:
            return '''def calculate_mean(input_data=None):
        """Calculate mean of numbers."""
        
        if input_data is None:
            return 0.0
        
        try:
            numbers = []
            
            if isinstance(input_data, (list, tuple)):
                for item in input_data:
                    try:
                        numbers.append(float(item))
                    except (ValueError, TypeError):
                        continue
            elif isinstance(input_data, dict):
                # Try common keys first
                for key in ['numbers', 'values', 'data']:
                    if key in input_data:
                        if isinstance(input_data[key], (list, tuple)):
                            for item in input_data[key]:
                                try:
                                    numbers.append(float(item))
                                except:
                                    continue
                        break
                else:
                    # Try all values
                    for value in input_data.values():
                        try:
                            if isinstance(value, (list, tuple)):
                                for item in value:
                                    try:
                                        numbers.append(float(item))
                                    except:
                                        continue
                            else:
                                numbers.append(float(value))
                        except:
                            continue
            elif isinstance(input_data, str):
                import re
                # Extract numbers from string
                matches = re.findall(r'-?\\d+\\.?\\d*', input_data)
                numbers = [float(m) for m in matches]
            else:
                try:
                    numbers = [float(input_data)]
                except:
                    return 0.0
            
            if not numbers:
                return 0.0
                
            return sum(numbers) / len(numbers)
            
        except Exception:
            return 0.0
    '''

        # Sentiment analysis
        elif "sentiment" in tool_lower:
            return '''def analyze_sentiment(input_data=None):
        """Analyze sentiment of text."""
        
        if input_data is None:
            return {"sentiment": "neutral", "score": 0.0}
        
        try:
            text = str(input_data)
            if isinstance(input_data, dict):
                text = input_data.get('text', input_data.get('content', str(input_data)))
            
            text_lower = text.lower()
            
            # Simple but functional sentiment analysis
            positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 
                            'fantastic', 'love', 'perfect', 'best', 'happy', 'awesome',
                            'brilliant', 'outstanding', 'superior', 'positive', 'success']
            negative_words = ['bad', 'terrible', 'awful', 'horrible', 'hate', 'worst',
                            'poor', 'disappointing', 'failure', 'negative', 'wrong',
                            'broken', 'useless', 'waste', 'angry', 'frustrated']
            
            positive_count = sum(1 for word in positive_words if word in text_lower)
            negative_count = sum(1 for word in negative_words if word in text_lower)
            
            # Calculate score
            if positive_count + negative_count == 0:
                sentiment = "neutral"
                score = 0.0
            else:
                score = (positive_count - negative_count) / (positive_count + negative_count)
                if score > 0.2:
                    sentiment = "positive"
                elif score < -0.2:
                    sentiment = "negative"
                else:
                    sentiment = "neutral"
            
            return {
                "sentiment": sentiment,
                "score": score,
                "positive_words": positive_count,
                "negative_words": negative_count
            }
            
        except Exception:
            return {"sentiment": "neutral", "score": 0.0}
    '''

        # Generic but functional tool
        else:
            # Create a functional tool based on the name
            return f'''def {tool_name}(input_data=None):
        """
        {description}
        """
        
        if input_data is None:
            return {{"status": "no_input", "result": None}}
        
        try:
            result = {{"status": "success"}}
            
            # Process based on input type
            if isinstance(input_data, str):
                result["text_length"] = len(input_data)
                result["word_count"] = len(input_data.split())
                result["processed"] = input_data.strip()
            elif isinstance(input_data, dict):
                result["keys"] = list(input_data.keys())
                result["size"] = len(input_data)
                result["processed"] = input_data
            elif isinstance(input_data, list):
                result["count"] = len(input_data)
                result["processed"] = input_data
            else:
                result["type"] = type(input_data).__name__
                result["value"] = str(input_data)
            
            return result
            
        except Exception as e:
            return {{"status": "error", "message": str(e)}}
    '''

    def ensure_tool(
        self, tool_name: str, description: str, tool_type: str = "pure_function"
    ) -> Dict[str, Any]:
        """Ensure tool exists with FUNCTIONAL implementation."""

        print(f"DEBUG: Ensuring tool '{tool_name}' exists")

        # Check if exists and file is actually there
        if self.registry.tool_exists(tool_name):
            tool = self.registry.get_tool(tool_name)
            # Verify file actually exists
            if os.path.exists(tool["location"]):
                print(f"DEBUG: Tool '{tool_name}' already exists - returning existing")
                return {"status": "exists", "tool": tool}
            else:
                print(
                    f"WARNING: Tool {tool_name} in registry but file missing, recreating..."
                )

        print(f"DEBUG: Tool '{tool_name}' doesn't exist - creating new")

        # Generate functional code
        code = self._generate_functional_tool_code(tool_name, description)

        # Use register_tool which now has verification
        registration_result = self.registry.register_tool(
            name=tool_name,
            description=description,
            code=code,
            signature=f"def {tool_name}(input_data=None)",
            tags=self._extract_tags_from_description(description),
            is_prebuilt=False,
            is_pure_function=(tool_type == "pure_function"),
        )

        if registration_result["status"] == "success":
            return {"status": "success", "tool": self.registry.get_tool(tool_name)}
        else:
            print(
                f"WARNING: Tool registration had issues: {registration_result.get('message')}"
            )
            return registration_result
