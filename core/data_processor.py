"""
Intelligent Data Processor
Uses GPT-4 for smart data extraction and preparation with comprehensive fallbacks
"""

import re
import json
import os
from typing import Any, Dict, List, Optional, Union
from openai import OpenAI
from config import OPENAI_API_KEY, ORCHESTRATOR_MODEL, ORCHESTRATOR_TEMPERATURE


class DataProcessor:
    """Intelligently extract and format data using GPT-4 with comprehensive fallbacks."""

    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

    def process_request_data(
        self, request: str, analysis: Dict = None
    ) -> Dict[str, Any]:
        """
        Extract and format data using GPT-4 intelligence with fallbacks.
        Returns multiple data formats for different agent needs.
        """

        print(f"DEBUG: Processing request data: {request[:100]}...")

        # Base data structure (always available)
        processed_data = {
            "raw_request": request,
            "raw_text": request,
            "current_data": request,
            "extracted_data": None,
            "data_type": "text",
            "extraction_method": "none",
        }

        # Try GPT-4 smart extraction first
        if self.client:
            gpt_extraction = self._gpt_smart_extraction(request, analysis)
            if gpt_extraction and gpt_extraction.get("extracted_data") is not None:
                processed_data.update(gpt_extraction)
                processed_data["extraction_method"] = "gpt4_smart"
                print(f"DEBUG: GPT-4 extracted: {gpt_extraction['extracted_data']}")
                return processed_data

        # Fallback: Comprehensive pattern-based extraction
        fallback_extraction = self._comprehensive_fallback_extraction(request)
        processed_data.update(fallback_extraction)
        processed_data["extraction_method"] = "pattern_fallback"

        print(f"DEBUG: Fallback extracted: {fallback_extraction.get('extracted_data')}")
        return processed_data

    def _gpt_smart_extraction(
        self, request: str, analysis: Dict = None
    ) -> Optional[Dict[str, Any]]:
        """Use GPT-4 to intelligently extract and format data from the request."""

        try:
            # Build context-aware prompt
            extraction_prompt = f"""You are a smart data extraction system. Analyze this user request and extract the specific data that needs processing.

USER REQUEST: "{request}"

ANALYSIS CONTEXT: {json.dumps(analysis, indent=2) if analysis else "No prior analysis available"}

EXTRACTION RULES:
1. Identify what specific data the user wants processed (not the task itself)
2. Extract and format that data appropriately for programmatic use
3. If multiple data items, return as appropriate collection type
4. If no specific data to extract, return the most relevant part of the request

EXAMPLES:
Request: "Find prime numbers in: 43, 17, 89, 56"
→ Extract: [43, 17, 89, 56]
→ Type: "number_array"

Request: "Count words in 'Hello world how are you today'"
→ Extract: "Hello world how are you today"  
→ Type: "text_string"

Request: "Extract emails from: Contact john@test.com or mary@example.org for support"
→ Extract: "Contact john@test.com or mary@example.org for support"
→ Type: "text_for_extraction"

Request: "Analyze these sales figures: Q1: $45K, Q2: $67K, Q3: $52K, Q4: $78K"
→ Extract: {{"Q1": 45000, "Q2": 67000, "Q3": 52000, "Q4": 78000}}
→ Type: "structured_data"

Request: "Process file data.csv and calculate averages"
→ Extract: "data.csv"
→ Type: "file_reference"

Request: "Is 97 a prime number?"
→ Extract: 97
→ Type: "single_number"

Respond with JSON:
{{
    "extracted_data": <the actual data to process>,
    "data_type": "<type classification>",
    "reasoning": "<brief explanation of what you extracted and why>",
    "format_notes": "<any special formatting considerations>"
}}

If no specific data can be extracted, return null for extracted_data."""

            response = self.client.chat.completions.create(
                model=ORCHESTRATOR_MODEL,
                max_completion_tokens=1000,
                messages=[{"role": "user", "content": extraction_prompt}],
            )

            # Parse GPT-4 response
            response_text = response.choices[0].message.content.strip()

            # Extract JSON from response
            if response_text.startswith("```json"):
                response_text = (
                    response_text.split("```json")[1].split("```")[0].strip()
                )
            elif response_text.startswith("```"):
                response_text = response_text.split("```")[1].split("```")[0].strip()

            extraction_result = json.loads(response_text)

            # Format the result for our system
            if extraction_result.get("extracted_data") is not None:
                formatted_result = {
                    "extracted_data": extraction_result["extracted_data"],
                    "current_data": extraction_result["extracted_data"],
                    "data_type": extraction_result.get("data_type", "unknown"),
                    "extraction_reasoning": extraction_result.get("reasoning", ""),
                    "format_notes": extraction_result.get("format_notes", ""),
                }

                print(
                    f"DEBUG: GPT-4 extraction successful - Type: {formatted_result['data_type']}"
                )
                print(
                    f"DEBUG: GPT-4 reasoning: {formatted_result['extraction_reasoning']}"
                )

                return formatted_result

        except Exception as e:
            print(f"DEBUG: GPT-4 extraction failed: {str(e)}")
            # Fall through to pattern-based fallback

        return None

    def _comprehensive_fallback_extraction(self, request: str) -> Dict[str, Any]:
        """Comprehensive fallback extraction handling ALL data types."""

        print(f"DEBUG: Using comprehensive fallback extraction")

        # Try all extraction methods in priority order
        extractors = [
            ("number_arrays", self._extract_number_arrays),
            ("single_numbers", self._extract_single_numbers),
            ("quoted_text", self._extract_quoted_text),
            ("structured_data", self._extract_structured_data),
            ("file_references", self._extract_file_references),
            ("email_addresses", self._extract_email_addresses),
            ("urls", self._extract_urls),
            ("dates", self._extract_dates),
            ("monetary_values", self._extract_monetary_values),
            ("percentages", self._extract_percentages),
            ("key_value_pairs", self._extract_key_value_pairs),
            ("code_blocks", self._extract_code_blocks),
            ("lists", self._extract_lists),
        ]

        for extractor_name, extractor_func in extractors:
            try:
                result = extractor_func(request)
                if result is not None:
                    print(f"DEBUG: Fallback extraction succeeded with {extractor_name}")
                    return {
                        "extracted_data": result,
                        "current_data": result,
                        "data_type": extractor_name,
                        "extraction_reasoning": f"Pattern-based extraction using {extractor_name}",
                    }
            except Exception as e:
                print(f"DEBUG: Extractor {extractor_name} failed: {str(e)}")
                continue

        # Final fallback: return the request as text
        print(f"DEBUG: All extractors failed, using raw text")
        return {
            "extracted_data": request,
            "current_data": request,
            "data_type": "raw_text",
            "extraction_reasoning": "No specific data patterns found, using full request text",
        }

    # ============================================================================
    # COMPREHENSIVE EXTRACTION METHODS
    # ============================================================================

    def _extract_number_arrays(self, text: str) -> Optional[List[Union[int, float]]]:
        """Extract arrays of numbers from text."""

        patterns = [
            r"(?:numbers?|list|values?|data)[:\s]*\[([^\]]+)\]",  # [1,2,3]
            r"(?:numbers?|list|values?|in)[:\s]*([0-9,.\s-]+)",  # 1, 2, 3
            r"(?:are|of)[:\s]*([0-9,.\s-]+)",  # are: 1, 2, 3
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                number_str = match.group(1)
                numbers = self._parse_numbers(number_str)
                if len(numbers) >= 2:  # Must be multiple numbers for an array
                    return numbers

        # Fallback: find all numbers if multiple exist
        all_numbers = re.findall(r"-?\d+(?:\.\d+)?", text)
        if len(all_numbers) >= 3:  # 3+ numbers likely indicate a list
            return self._parse_numbers(", ".join(all_numbers))

        return None

    def _extract_single_numbers(self, text: str) -> Optional[Union[int, float]]:
        """Extract single numbers from text."""

        # Look for patterns like "Is 97 a prime" or "check number 42"
        patterns = [
            r"(?:is|check|number|value)\s+(\d+(?:\.\d+)?)",
            r"(\d+(?:\.\d+)?)\s+(?:a|is|prime|even|odd)",
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                num_str = match.group(1)
                return float(num_str) if "." in num_str else int(num_str)

        return None

    def _extract_quoted_text(self, text: str) -> Optional[str]:
        """Extract text from various quote formats."""

        patterns = [
            r'"([^"]+)"',  # Double quotes
            r"'([^']+)'",  # Single quotes
            r"`([^`]+)`",  # Backticks
            r"â€œ([^â€]+)â€",  # Smart quotes
            r"<<([^>]+)>>",  # Angle brackets
        ]

        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                # Return the longest match (likely the main content)
                return max(matches, key=len)

        return None

    def _extract_structured_data(self, text: str) -> Optional[Dict]:
        """Extract structured data like key-value pairs."""

        # Pattern for "Q1: $45K, Q2: $67K" style data
        kv_pattern = r"([A-Za-z0-9_]+)[:\s]*([^,\n]+)"
        matches = re.findall(kv_pattern, text)

        if len(matches) >= 2:  # Need multiple pairs for structured data
            result = {}
            for key, value in matches:
                # Try to parse value as number
                clean_value = re.sub(r"[^\d.-]", "", value.strip())
                if (
                    clean_value
                    and clean_value.replace(".", "").replace("-", "").isdigit()
                ):
                    # Handle currency/units (K, M, B)
                    multiplier = 1
                    if "K" in value.upper():
                        multiplier = 1000
                    elif "M" in value.upper():
                        multiplier = 1000000
                    elif "B" in value.upper():
                        multiplier = 1000000000

                    result[key] = float(clean_value) * multiplier
                else:
                    result[key] = value.strip()

            return result if result else None

        return None

    def _extract_file_references(self, text: str) -> Optional[Union[str, List[str]]]:
        """Extract file references and paths."""

        patterns = [
            r"(?:file|document|path)[:\s]*([^\s]+\.(?:csv|pdf|txt|json|xlsx?|doc|png|jpg))",
            r"([^\s]+\.(?:csv|pdf|txt|json|xlsx?|doc|png|jpg))",
            r"(?:process|read|analyze)[:\s]*([^\s]+\.(?:csv|pdf|txt|json|xlsx?))",
        ]

        files = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            files.extend(matches)

        if files:
            return files[0] if len(files) == 1 else list(set(files))

        return None

    def _extract_email_addresses(self, text: str) -> Optional[List[str]]:
        """Extract email addresses for processing."""

        email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        emails = re.findall(email_pattern, text)

        # If emails found and request is about email processing, return them
        if emails and any(
            word in text.lower() for word in ["email", "extract", "find"]
        ):
            return list(set(emails))

        return None

    def _extract_urls(self, text: str) -> Optional[List[str]]:
        """Extract URLs for processing."""

        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        urls = re.findall(url_pattern, text)

        if urls and any(
            word in text.lower() for word in ["url", "link", "website", "extract"]
        ):
            return list(set(urls))

        return None

    def _extract_dates(self, text: str) -> Optional[List[str]]:
        """Extract date patterns."""

        date_patterns = [
            r"\d{1,2}[-/]\d{1,2}[-/]\d{2,4}",  # MM/DD/YYYY or MM-DD-YYYY
            r"\d{4}[-/]\d{1,2}[-/]\d{1,2}",  # YYYY-MM-DD
            r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}",  # Month DD, YYYY
        ]

        dates = []
        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            dates.extend(matches)

        if dates and any(
            word in text.lower() for word in ["date", "when", "time", "schedule"]
        ):
            return list(set(dates))

        return None

    def _extract_monetary_values(self, text: str) -> Optional[List[Union[int, float]]]:
        """Extract monetary values."""

        money_pattern = r"\$\s*(\d+(?:,\d{3})*(?:\.\d{2})?)\s*([KMB]?)"
        matches = re.findall(money_pattern, text)

        if matches:
            values = []
            for amount, unit in matches:
                value = float(amount.replace(",", ""))
                if unit.upper() == "K":
                    value *= 1000
                elif unit.upper() == "M":
                    value *= 1000000
                elif unit.upper() == "B":
                    value *= 1000000000
                values.append(value)
            return values

        return None

    def _extract_percentages(self, text: str) -> Optional[List[float]]:
        """Extract percentage values."""

        percent_pattern = r"(\d+(?:\.\d+)?)\s*%"
        matches = re.findall(percent_pattern, text)

        if matches:
            return [float(match) for match in matches]

        return None

    def _extract_key_value_pairs(self, text: str) -> Optional[Dict[str, Any]]:
        """Extract key-value pairs from various formats."""

        # JSON-like patterns
        json_pattern = r"\{[^}]+\}"
        json_match = re.search(json_pattern, text)
        if json_match:
            try:
                return json.loads(json_match.group())
            except:
                pass

        # Simple key: value patterns
        kv_patterns = [
            r"(\w+):\s*([^,\n]+)",
            r"(\w+)\s*=\s*([^,\n]+)",
        ]

        for pattern in kv_patterns:
            matches = re.findall(pattern, text)
            if len(matches) >= 2:
                return dict(matches)

        return None

    def _extract_code_blocks(self, text: str) -> Optional[str]:
        """Extract code blocks."""

        patterns = [
            r"```(?:python|js|javascript|html|css)?\n(.*?)\n```",
            r"`([^`]+)`",
            r"<code>(.*?)</code>",
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL)
            if match:
                return match.group(1).strip()

        return None

    def _extract_lists(self, text: str) -> Optional[List[str]]:
        """Extract list items from various formats."""

        # Bullet point lists
        bullet_pattern = r"(?:^|\n)\s*[-•*]\s*([^\n]+)"
        bullets = re.findall(bullet_pattern, text, re.MULTILINE)

        if bullets:
            return [item.strip() for item in bullets]

        # Numbered lists
        numbered_pattern = r"(?:^|\n)\s*\d+\.?\s*([^\n]+)"
        numbered = re.findall(numbered_pattern, text, re.MULTILINE)

        if numbered:
            return [item.strip() for item in numbered]

        # Comma-separated lists (non-numeric)
        if "," in text and not re.search(r"\d+,\s*\d+", text):
            parts = [part.strip() for part in text.split(",")]
            if len(parts) >= 3 and all(len(part) > 2 for part in parts[:3]):
                return parts

        return None

    def _parse_numbers(self, number_string: str) -> List[Union[int, float]]:
        """Parse a string containing multiple numbers."""

        numbers = []
        for match in re.findall(r"-?\d+(?:\.\d+)?", number_string):
            if "." in match:
                numbers.append(float(match))
            else:
                numbers.append(int(match))
        return numbers
