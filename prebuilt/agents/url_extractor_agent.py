def url_extractor_agent(state):
    """
    Extract URLs from input text.
    """
    import sys
    import os
    from datetime import datetime

    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # Import tool
    from generated.tools.extract_urls import extract_urls

    # Initialize state
    if "results" not in state:
        state["results"] = {}
    if "errors" not in state:
        state["errors"] = []
    if "execution_path" not in state:
        state["execution_path"] = []

    try:
        start_time = datetime.now()

        # Extract input
        input_data = state.get("current_data")
        if input_data is None:
            input_data = state.get("text", state.get("data", state.get("request", "")))

        # Process with tool
        urls = extract_urls(input_data)

        # Analyze URLs
        domains = {}
        for url in urls:
            try:
                from urllib.parse import urlparse

                parsed = urlparse(url)
                domain = parsed.netloc or parsed.path.split("/")[0]
                domains[domain] = domains.get(domain, 0) + 1
            except:
                pass

        # Create result
        result = {
            "status": "success",
            "data": {"urls": urls, "count": len(urls), "domains": domains},
            "metadata": {
                "agent": "url_extractor",
                "execution_time": (datetime.now() - start_time).total_seconds(),
                "tools_used": ["extract_urls"],
            },
        }

        # Update state
        state["results"]["url_extractor"] = result
        state["current_data"] = result["data"]
        state["execution_path"].append("url_extractor")

    except Exception as e:
        state["errors"].append({"agent": "url_extractor", "error": str(e)})
        state["results"]["url_extractor"] = {
            "status": "error",
            "data": None,
            "metadata": {"agent": "url_extractor", "error": str(e)},
        }

    return state
