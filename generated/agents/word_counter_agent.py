def word_counter_agent(state):
    """
    Use the count_words tool to count the number of words in a provided text
    """
    import sys
    import os
    from datetime import datetime

    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # Import tools
    try:
        from generated.tools.count_words import count_words
    except ImportError:
        try:
            from prebuilt.tools.count_words import count_words
        except ImportError:
            # Define fallback if tool not found
            def count_words(input_data=None):
                return {"error": "Tool count_words not found", "data": None}

    # Initialize state
    if "results" not in state:
        state["results"] = {}
    if "errors" not in state:
        state["errors"] = []
    if "execution_path" not in state:
        state["execution_path"] = []

    try:
        start_time = datetime.now()

        # Get input data using standard pattern
        input_data = state.get("current_data")
        if input_data is None:
            if "results" in state and state["execution_path"]:
                last_agent = state["execution_path"][-1]
                if last_agent in state["results"]:
                    last_result = state["results"][last_agent]
                    if isinstance(last_result, dict) and "data" in last_result:
                        input_data = last_result["data"]

        if input_data is None:
            input_data = state.get("text", state.get("data", state.get("request")))

        import re

        target_text = input_data
        if isinstance(input_data, str):
            # Look for text in quotes (the actual text to count)
            quote_patterns = [
                r'"([^"]+)"',  # Double quotes
                r"'([^']+)'",  # Single quotes
            ]

            for pattern in quote_patterns:
                matches = re.findall(pattern, input_data)
                if matches:
                    # Use the last quoted text found (likely the target)
                    target_text = matches[-1]
                    break

        # Then use target_text instead of input_data:
        tool_result = count_words(target_text)
        if isinstance(tool_result, dict):
            word_count = tool_result.get("word_count", tool_result.get("data", 0))
        else:
            word_count = tool_result if isinstance(tool_result, int) else 0

        # Create meaningful output
        result = {
            "status": "success",
            "data": {
                "word_count": word_count,
                "input_length": len(input_data.split()),
                "input_text": input_data,
            },
            "metadata": {
                "agent": "word_counter",
                "execution_time": (datetime.now() - start_time).total_seconds(),
                "tools_used": ["count_words"],
            },
        }

        state["results"]["word_counter"] = result
        state["current_data"] = result["data"]
        state["execution_path"].append("word_counter")

    except Exception as e:
        import traceback

        state["errors"].append(
            {
                "agent": "word_counter",
                "error": str(e),
                "traceback": traceback.format_exc(),
            }
        )
        state["results"]["word_counter"] = {
            "status": "error",
            "data": None,
            "metadata": {"agent": "word_counter", "error": str(e)},
        }

    return state
