def url_extractor_agent(state):
    """
    Agent that extracts URLs from input text.
    Uses extract_urls tool to find all URLs.
    """
    import sys
    import os
    from datetime import datetime

    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    from generated.tools.extract_urls import extract_urls

    # Initialize state components
    if "results" not in state:
        state["results"] = {}
    if "errors" not in state:
        state["errors"] = []
    if "execution_path" not in state:
        state["execution_path"] = []

    try:
        start_time = datetime.now()

        # Extract input data flexibly
        input_data = None

        # Check current_data first
        current_data = state.get("current_data")
        if current_data is not None:
            if isinstance(current_data, str):
                input_data = current_data
            elif isinstance(current_data, dict):
                for key in ["text", "data", "content", "value", "result"]:
                    if key in current_data:
                        input_data = current_data[key]
                        break
                if input_data is None:
                    input_data = current_data
            else:
                input_data = current_data

        # Check previous results
        if input_data is None and "results" in state:
            for result in reversed(list(state["results"].values())):
                if isinstance(result, dict) and "data" in result:
                    input_data = result["data"]
                    break

        # Check root state
        if input_data is None:
            for key in ["text", "data", "input", "request"]:
                if key in state and state[key]:
                    input_data = state[key]
                    break

        # Process with tool
        urls = extract_urls(input_data)

        # Calculate execution time
        execution_time = (datetime.now() - start_time).total_seconds()

        # Create standard output envelope
        result = {
            "status": "success",
            "data": {
                "urls": urls,
                "count": len(urls),
                "unique_domains": list(
                    set(url.split("/")[2] for url in urls if "/" in url)
                ),
            },
            "metadata": {
                "agent": "url_extractor",
                "execution_time": execution_time,
                "tools_used": ["extract_urls"],
                "warnings": [],
            },
        }

        # Update state
        state["results"]["url_extractor"] = result
        state["current_data"] = result["data"]
        state["execution_path"].append("url_extractor")

    except Exception as e:
        import traceback

        error_detail = {
            "agent": "url_extractor",
            "error": str(e),
            "traceback": traceback.format_exc(),
            "timestamp": datetime.now().isoformat(),
        }
        state["errors"].append(error_detail)

        state["results"]["url_extractor"] = {
            "status": "error",
            "data": None,
            "metadata": {
                "agent": "url_extractor",
                "execution_time": 0,
                "error": str(e),
            },
        }

    return state
