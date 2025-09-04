def word_counter_agent(state):
    """
    Count words in text using the count_words tool
    """
    import sys
    import os
    from datetime import datetime

    # MANDATORY: Add path for imports
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # MANDATORY: Import required tools (if any)
    from generated.tools.count_words import count_words

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

        # Priority 1: Check current_data
        current_data = state.get('current_data')
        if current_data is not None:
            if isinstance(current_data, str):
                input_data = current_data
            elif isinstance(current_data, dict):
                for key in ['text', 'data', 'content', 'value', 'result']:
                    if key in current_data:
                        input_data = current_data[key]
                        break
                if input_data is None:
                    input_data = current_data
            else:
                input_data = str(current_data)

        # Priority 2: Check previous results
        if input_data is None and 'results' in state:
            for result in reversed(list(state['results'].values())):
                if isinstance(result, dict) and 'data' in result:
                    input_data = result['data']
                    break

        # Priority 3: Check root state
        if input_data is None:
            for key in ['text', 'data', 'input', 'request']:
                if key in state and state[key]:
                    input_data = state[key]
                    break

        # AGENT LOGIC: Process input_data using tools
        processed_data = {}
        tool_result = count_words(input_data)
        processed_data['count_words_result'] = tool_result

        # Calculate execution time
        execution_time = (datetime.now() - start_time).total_seconds()

        # MANDATORY: Standard output envelope
        result = {
            "status": "success",
            "data": processed_data,
            "metadata": {
                "agent": "word_counter",
                "execution_time": execution_time,
                "tools_used": ["count_words"],
                "warnings": []
            }
        }

        # MANDATORY: Update state
        state['results']['word_counter'] = result
        state['current_data'] = result['data']
        state['execution_path'].append('word_counter')

    except Exception as e:
        import traceback
        error_detail = {
            "agent": "word_counter",
            "error": str(e),
            "traceback": traceback.format_exc(),
            "timestamp": datetime.now().isoformat()
        }
        state['errors'].append(error_detail)

        state['results']['word_counter'] = {
            "status": "error",
            "data": None,
            "metadata": {
                "agent": "word_counter",
                "execution_time": 0,
                "error": str(e)
            }
        }

    return state