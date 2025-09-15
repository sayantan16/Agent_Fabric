"""
Enhanced Intelligent Agent Base
Each agent has Claude reasoning capabilities
"""

import json
from typing import Dict, Any, List, Optional
from anthropic import Anthropic
import os

from config import CLAUDE_MODEL


class IntelligentAgent:
    """Base agent with Claude reasoning capabilities"""

    def __init__(self, name: str, purpose: str, tools: List[str] = None):
        self.name = name
        self.purpose = purpose
        self.tools = tools or []
        self.claude = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    async def execute(self, state: Dict) -> Dict:
        """Execute with intelligent reasoning"""

        # Step 1: Understand what we received
        analysis = await self.analyze_input(state)

        # Step 2: Process based on analysis
        result = await self.process_with_reasoning(state, analysis)

        # Step 3: Format output for next agent
        formatted = await self.format_output(result, state)

        return formatted

    async def analyze_input(self, state: Dict) -> Dict:
        """Claude analyzes input data"""

        current_data = state.get("current_data", {})

        # Format data for Claude
        if isinstance(current_data, dict) and "columns" in current_data:
            # CSV data
            data_desc = f"CSV with columns: {current_data['columns']}, {current_data.get('total_rows', 0)} rows"
        else:
            data_desc = str(type(current_data).__name__)

        prompt = f"""
        I am agent '{self.name}' with purpose: {self.purpose}
        
        I received: {data_desc}
        Data sample: {str(current_data)[:500]}
        
        Analyze:
        1. What type of data is this?
        2. What should I do with it?
        3. What would be useful output?
        
        Be specific and concise.
        """

        response = self.claude.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )

        return {"analysis": response.content[0].text}

    async def process_with_reasoning(self, state: Dict, analysis: Dict) -> Dict:
        """Process data with Claude's guidance"""

        prompt = f"""
        Based on analysis: {analysis['analysis']}
        
        Process this data for: {self.purpose}
        Available tools: {self.tools}
        
        Current data: {str(state.get('current_data'))[:1000]}
        
        Provide the processed result.
        """

        response = self.claude.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}],
        )

        return {
            "processed_data": response.content[0].text,
            "reasoning": analysis["analysis"],
        }

    async def format_output(self, result: Dict, original_state: Dict) -> Dict:
        """Format output for pipeline"""

        return {
            "status": "success",
            "agent": self.name,
            "data": result.get("processed_data"),
            "reasoning": result.get("reasoning"),
            "metadata": {
                "input_type": type(original_state.get("current_data")).__name__,
                "purpose": self.purpose,
                "tools_used": self.tools,
            },
        }


class DataAnalysisAgent(IntelligentAgent):
    """Specialized agent for data analysis"""

    def __init__(self):
        super().__init__(
            name="data_analysis",
            purpose="Analyze data patterns and extract insights",
            tools=["pandas", "statistics"],
        )

    async def process_with_reasoning(self, state: Dict, analysis: Dict) -> Dict:
        """Specialized processing for data analysis"""

        current_data = state.get("current_data", {})

        if isinstance(current_data, dict) and "columns" in current_data:
            # Work with CSV data
            prompt = f"""
            Analyze this CSV data:
            Columns: {current_data['columns']}
            Sample rows: {current_data.get('first_10_rows', [])[:3]}
            Total rows: {current_data.get('total_rows', 0)}
            
            Provide:
            1. Key statistics
            2. Data patterns
            3. Interesting insights
            4. Potential issues
            """

            response = self.claude.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}],
            )

            return {
                "processed_data": response.content[0].text,
                "reasoning": "Analyzed CSV data structure and patterns",
            }

        # Default processing
        return await super().process_with_reasoning(state, analysis)
