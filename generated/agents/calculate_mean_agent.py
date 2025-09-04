def calculate_mean_agent(state):
    """
    Process calculate_mean tasks
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
        # Process input data
        # No tools specified - process input directly
        if isinstance(input_data, (list, tuple)):
            processed_data = {'mean': sum(input_data) / len(input_data)}
        elif isinstance(input_data, (int, float)):
            processed_data = {'mean': input_data}
        else:
            processed_data = {'result': 'No numeric input provided'}

        # Calculate execution time
        execution_time = (datetime.now() - start_time).total_seconds()

        # MANDATORY: Standard output envelope
        result = {
            "status": "success",
            "data": processed_data,
            "metadata": {
                "agent": "calculate_mean",
                "execution_time": execution_time,
                "tools_used": [],
                "warnings": []
            }
        }

        # MANDATORY: Update state
        state['results']['calculate_mean'] = result
        state['current_data'] = result['data']
        state['execution_path'].append('calculate_mean')

    except Exception as e:
        import traceback
        error_detail = {
            "agent": "calculate_mean",
            "error": str(e),
            "traceback": traceback.format_exc(),
            "timestamp": datetime.now().isoformat()
        }
        state['errors'].append(error_detail)

        state['results']['calculate_mean'] = {
            "status": "error",
            "data": None,
            "metadata": {
                "agent": "calculate_mean",
                "execution_time": 0,
                "error": str(e)
            }
        }

    return state