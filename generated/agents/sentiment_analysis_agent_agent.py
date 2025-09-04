def sentiment_analysis_agent(state):
    """
    Perform sentiment analysis on customer feedback text
    """
    import sys
    import os
    from datetime import datetime

    # MANDATORY: Add path for imports
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # MANDATORY: Import required tools (if any)
    from generated.tools.analyze_sentiment import analyze_sentiment

    # MANDATORY: Initialize state components
    if 'results' not in state:
        state['results'] = {}
    if 'errors' not in state:
        state['errors'] = []
    if 'execution_path' not in state:
        state['execution_path'] = []

    try:
        start_time = datetime.now()

        # MANDATORY: Universal input extraction
        input_data = None
        if 'current_data' in state:
            input_data = state['current_data']
        elif 'results' in state:
            for result in reversed(list(state['results'].values())):
                if isinstance(result, dict) and 'data' in result:
                    input_data = result['data']
                    break
        elif 'text' in state:
            input_data = state['text']

        # AGENT LOGIC: Process input_data using tools
        if input_data:
            sentiment_result = analyze_sentiment(input_data)
            processed_data = {
                "sentiment_label": sentiment_result["sentiment_label"],
                "sentiment_score": sentiment_result["sentiment_score"]
            }
        else:
            processed_data = {}

        # Calculate execution time
        execution_time = (datetime.now() - start_time).total_seconds()

        # MANDATORY: Standard output envelope
        result = {
            "status": "success",
            "data": processed_data,
            "metadata": {
                "agent": "sentiment_analysis_agent",
                "execution_time": execution_time,
                "tools_used": ["analyze_sentiment"],
                "warnings": []
            }
        }

        # MANDATORY: Update state
        state['results']['sentiment_analysis_agent'] = result
        state['current_data'] = result['data']
        state['execution_path'].append('sentiment_analysis_agent')

    except Exception as e:
        import traceback
        error_detail = {
            "agent": "sentiment_analysis_agent",
            "error": str(e),
            "traceback": traceback.format_exc(),
            "timestamp": datetime.now().isoformat()
        }
        state['errors'].append(error_detail)

        state['results']['sentiment_analysis_agent'] = {
            "status": "error",
            "data": None,
            "metadata": {
                "agent": "sentiment_analysis_agent",
                "execution_time": 0,
                "error": str(e)
            }
        }

    return state