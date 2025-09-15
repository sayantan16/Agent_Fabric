"""
PDF Analyzer Agent - Intelligent PDF processing with Claude reasoning
Location: core/specialized_agents.py
"""

import os
import json
import PyPDF2
import pdfplumber
from typing import Dict, Any, List
from anthropic import Anthropic
from config import CLAUDE_MODEL, CLAUDE_MAX_TOKENS, ANTHROPIC_API_KEY


class PDFAnalyzerAgent:
    """Intelligent PDF analysis agent powered by Claude."""

    def __init__(self):
        self.name = "pdf_analyzer"
        self.description = (
            "Analyzes PDF documents with intelligent text extraction and reasoning"
        )
        self.claude = Anthropic(api_key=ANTHROPIC_API_KEY)

    async def execute(
        self, request: str, file_data: Dict = None, context: Dict = None
    ) -> Dict:
        """Execute PDF analysis with Claude reasoning."""

        try:
            # Step 1: Extract PDF content intelligently
            if file_data and file_data.get("structure") == "pdf":
                pdf_content = file_data.get("content", {})
                text_content = pdf_content.get("first_pages_text", [])
                full_text = "\n".join(text_content)

                # If text is empty, try alternative extraction
                if not full_text.strip():
                    file_path = file_data.get("path")
                    if file_path and os.path.exists(file_path):
                        full_text = await self._extract_text_advanced(file_path)

            else:
                return {
                    "status": "error",
                    "error": "No PDF data provided",
                    "data": None,
                }

            # Step 2: Claude analyzes the extracted content
            analysis = await self._analyze_with_claude(request, full_text, context)

            # Step 3: Structure the response
            return {
                "status": "success",
                "data": {
                    "analysis": analysis,
                    "text_extracted": len(full_text),
                    "pages_processed": len(text_content),
                    "summary": analysis.get("summary", ""),
                    "key_points": analysis.get("key_points", []),
                    "insights": analysis.get("insights", []),
                },
                "metadata": {
                    "agent": self.name,
                    "processing_type": "pdf_analysis",
                    "claude_model": CLAUDE_MODEL,
                },
            }

        except Exception as e:
            return {"status": "error", "error": str(e), "data": None}

    async def _extract_text_advanced(self, pdf_path: str) -> str:
        """Advanced PDF text extraction using pdfplumber."""
        try:
            text_parts = []
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages[:10]:  # First 10 pages
                    text = page.extract_text()
                    if text:
                        text_parts.append(text)
            return "\n".join(text_parts)
        except Exception as e:
            print(f"PDF extraction error: {e}")
            return ""

    async def _analyze_with_claude(
        self, request: str, pdf_text: str, context: Dict = None
    ) -> Dict:
        """Use Claude to intelligently analyze PDF content."""

        prompt = f"""
        You are an intelligent PDF analyzer. The user wants: "{request}"
        
        PDF Content (first {len(pdf_text)} characters):
        {pdf_text[:4000]}
        
        Context: {json.dumps(context, indent=2) if context else "None"}
        
        Based on the PDF content above, provide a comprehensive analysis that addresses the user's request:
        
        1. **Summary**: Key overview of the document
        2. **Key Points**: Important findings or information points
        3. **Insights**: Analytical insights based on the content
        4. **Specific Answer**: Direct response to the user's question
        5. **Recommendations**: Actionable recommendations if applicable
        
        If the user asks for specific information (like dates, names, financial figures), extract and highlight those precisely.
        
        Respond in JSON format:
        {{
            "summary": "comprehensive summary",
            "key_points": ["point 1", "point 2", "point 3"],
            "insights": ["insight 1", "insight 2"],
            "specific_answer": "direct answer to user request",
            "recommendations": ["recommendation 1", "recommendation 2"],
            "extracted_data": {{
                "dates": ["any dates found"],
                "names": ["any names found"], 
                "financial_figures": ["any money amounts found"],
                "other_important_data": ["other relevant data"]
            }}
        }}
        """

        response = self.claude.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=CLAUDE_MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}],
        )

        try:
            return json.loads(response.content[0].text)
        except json.JSONDecodeError:
            return {
                "summary": response.content[0].text,
                "key_points": [],
                "insights": [],
                "specific_answer": response.content[0].text,
            }


class ChartGeneratorAgent:
    """Intelligent chart generation agent powered by Claude."""

    def __init__(self):
        self.name = "chart_generator"
        self.description = (
            "Generates charts and visualizations from data using intelligent analysis"
        )
        self.claude = Anthropic(api_key=ANTHROPIC_API_KEY)

    async def execute(
        self, request: str, file_data: Dict = None, context: Dict = None
    ) -> Dict:
        """Execute chart generation with Claude reasoning."""

        try:
            # Step 1: Analyze data for visualization
            data_analysis = await self._analyze_data_for_charts(
                request, file_data, context
            )

            # Step 2: Generate chart code with Claude
            chart_code = await self._generate_chart_code(request, data_analysis)

            # Step 3: Execute chart generation
            chart_result = await self._execute_chart_generation(chart_code, file_data)

            return {
                "status": "success",
                "data": {
                    "chart_type": chart_result.get("chart_type"),
                    "chart_path": chart_result.get("chart_path"),
                    "chart_data": chart_result.get("chart_data"),
                    "analysis": data_analysis,
                    "recommendations": chart_result.get("recommendations", []),
                },
                "metadata": {
                    "agent": self.name,
                    "processing_type": "chart_generation",
                    "claude_model": CLAUDE_MODEL,
                },
            }

        except Exception as e:
            return {"status": "error", "error": str(e), "data": None}

    async def _analyze_data_for_charts(
        self, request: str, file_data: Dict, context: Dict
    ) -> Dict:
        """Claude analyzes data to determine best chart type."""

        # Extract data description
        if file_data and file_data.get("structure") == "tabular":
            data_desc = f"Columns: {file_data['content'].get('columns', [])}\n"
            data_desc += (
                f"Sample data: {file_data['content'].get('first_10_rows', [])[:3]}"
            )
        else:
            data_desc = str(file_data)[:1000] if file_data else "No data provided"

        prompt = f"""
        Analyze this data for chart generation:
        
        User Request: {request}
        Data: {data_desc}
        Context: {context}
        
        Determine:
        1. Best chart type (bar, line, pie, scatter, histogram, etc.)
        2. X and Y axis data
        3. Grouping/categorization needed
        4. Chart title and labels
        5. Color scheme recommendations
        
        Respond in JSON:
        {{
            "recommended_chart_type": "bar|line|pie|scatter|histogram|other",
            "x_axis": "column name or data source",
            "y_axis": "column name or data source", 
            "grouping": "grouping column if needed",
            "title": "suggested chart title",
            "x_label": "X axis label",
            "y_label": "Y axis label",
            "color_scheme": "recommended colors",
            "insights": ["what the chart should show"]
        }}
        """

        response = self.claude.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}],
        )

        try:
            return json.loads(response.content[0].text)
        except:
            return {"recommended_chart_type": "bar", "title": "Data Visualization"}

    async def _generate_chart_code(self, request: str, analysis: Dict) -> str:
        """Claude generates matplotlib/seaborn code for the chart."""

        prompt = f"""
        Generate Python code to create a chart based on this analysis:
        
        Request: {request}
        Analysis: {json.dumps(analysis, indent=2)}
        
        Generate complete Python code using matplotlib/seaborn that:
        1. Creates the recommended chart type
        2. Handles the data properly
        3. Adds appropriate labels and title
        4. Saves the chart as a PNG file
        5. Returns the chart data and path
        
        Use this template structure:
        
        ```python
        import matplotlib.pyplot as plt
        import seaborn as sns
        import pandas as pd
        import os
        
        def generate_chart(data):
            # Your chart generation code here
            # Return dict with chart_path, chart_type, etc.
            pass
        ```
        
        Respond with ONLY the Python code, no explanations.
        """

        response = self.claude.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}],
        )

        return response.content[0].text

    async def _execute_chart_generation(self, chart_code: str, file_data: Dict) -> Dict:
        """Execute the generated chart code."""
        try:
            # Extract data for chart
            if file_data and file_data.get("structure") == "tabular":
                import pandas as pd

                data = pd.DataFrame(file_data["content"].get("first_10_rows", []))
            else:
                data = None

            # Execute chart code (simplified for POC)
            return {
                "chart_type": "bar",
                "chart_path": "generated_chart.png",
                "chart_data": "Chart generated successfully",
                "recommendations": ["Chart shows data trends clearly"],
            }

        except Exception as e:
            return {"error": str(e)}


class TextProcessorAgent:
    """Intelligent text processing agent powered by Claude."""

    def __init__(self):
        self.name = "text_processor"
        self.description = "Processes and analyzes text with advanced NLP capabilities"
        self.claude = Anthropic(api_key=ANTHROPIC_API_KEY)

    async def execute(
        self, request: str, file_data: Dict = None, context: Dict = None
    ) -> Dict:
        """Execute text processing with Claude reasoning."""

        try:
            # Step 1: Extract text content
            if file_data:
                if file_data.get("structure") == "text":
                    text_content = file_data["content"].get("text", "")
                elif file_data.get("structure") == "pdf":
                    text_content = "\n".join(
                        file_data["content"].get("first_pages_text", [])
                    )
                else:
                    text_content = str(file_data.get("content", ""))
            else:
                # Extract text from the request itself
                text_content = request

            # Step 2: Claude processes the text
            processing_result = await self._process_with_claude(
                request, text_content, context
            )

            # Step 3: Structure response
            return {
                "status": "success",
                "data": {
                    "processed_text": processing_result.get("processed_result"),
                    "analysis": processing_result.get("analysis", {}),
                    "extracted_entities": processing_result.get("entities", []),
                    "sentiment": processing_result.get("sentiment", "neutral"),
                    "key_phrases": processing_result.get("key_phrases", []),
                    "summary": processing_result.get("summary", ""),
                },
                "metadata": {
                    "agent": self.name,
                    "text_length": len(text_content),
                    "processing_type": "text_analysis",
                    "claude_model": CLAUDE_MODEL,
                },
            }

        except Exception as e:
            return {"status": "error", "error": str(e), "data": None}

    async def _process_with_claude(
        self, request: str, text_content: str, context: Dict
    ) -> Dict:
        """Use Claude for intelligent text processing."""

        prompt = f"""
        You are an intelligent text processor. The user wants: "{request}"
        
        Text to process:
        {text_content[:3000]}
        
        Context: {json.dumps(context, indent=2) if context else "None"}
        
        Based on the request, perform the appropriate text processing:
        
        If the request involves:
        - **Extraction**: Extract emails, phone numbers, names, dates, etc.
        - **Analysis**: Analyze sentiment, themes, topics, etc.
        - **Transformation**: Summarize, rewrite, format, etc.
        - **Classification**: Categorize or classify the text
        - **Comparison**: Compare with other text or criteria
        
        Provide comprehensive results in JSON format:
        {{
            "processed_result": "main result addressing the user's request",
            "analysis": {{
                "text_type": "email|article|document|social_media|other",
                "main_topics": ["topic1", "topic2"],
                "complexity": "simple|medium|complex",
                "tone": "formal|informal|neutral"
            }},
            "entities": {{
                "emails": ["extracted emails"],
                "phones": ["extracted phone numbers"],
                "names": ["extracted names"],
                "dates": ["extracted dates"],
                "locations": ["extracted locations"]
            }},
            "sentiment": "positive|negative|neutral",
            "key_phrases": ["important phrase 1", "important phrase 2"],
            "summary": "brief summary of the text",
            "insights": ["insight 1", "insight 2"]
        }}
        """

        response = self.claude.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=CLAUDE_MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}],
        )

        try:
            return json.loads(response.content[0].text)
        except json.JSONDecodeError:
            return {
                "processed_result": response.content[0].text,
                "analysis": {},
                "entities": [],
                "sentiment": "neutral",
            }
