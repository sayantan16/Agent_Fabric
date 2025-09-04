def read_text_agent(state):
    """
    Process read_text tasks
    """
    import sys
    import os
    from datetime import datetime

    # MANDATORY: Add path for imports
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # MANDATORY: Import required tools (if any)
    # No tools to import

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
        # Implement the agent logic here
        processed_data = {
            "original_text": input_data,
            "processed_text": input_data.strip().replace("\n", " ")
        }

        # Calculate execution time
        execution_time = (datetime.now() - start_time).total_seconds()

        # MANDATORY: Standard output envelope
        result = {
            "status": "success",
            "data": processed_data,
            "metadata": {
                "agent": "read_text",
                "execution_time": execution_time,
                "tools_used": [],
                "warnings": []
            }
        }

        # MANDATORY: Update state
        state['results']['read_text'] = result
        state['current_data'] = result['data']
        state['execution_path'].append('read_text')

    except Exception as e:
        import traceback
        error_detail = {
            "agent": "read_text",
            "error": str(e),
            "traceback": traceback.format_exc(),
            "timestamp": datetime.now().isoformat()
        }
        state['errors'].append(error_detail)

        state['results']['read_text'] = {
            "status": "error",
            "data": None,
            "metadata": {
                "agent": "read_text",
                "execution_time": 0,
                "error": str(e)
            }
        }

    return state