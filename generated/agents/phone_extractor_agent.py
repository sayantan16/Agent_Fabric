def phone_extractor_agent(state):
    """
    Process phone_extractor tasks
    """
    import sys
    import os
    import re
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

        # AGENT LOGIC: Process input_data using tools
        if input_data:
            # Preprocess the input
            input_data = re.sub(r'\s+', ' ', input_data.strip())

            # Extract phone numbers
            phone_pattern = r'\b\+?\d{1,3}[-. ]?\(?\d{1,3}\)?[-. ]?\d{3,4}[-. ]?\d{4}\b'
            phone_numbers = re.findall(phone_pattern, input_data)

            # Filter and format the phone numbers
            processed_data = {
                'phone_numbers': [
                    re.sub(r'[^+\d]', '', num)
                    for num in phone_numbers
                    if len(re.sub(r'[^+\d]', '', num)) in [10, 11, 12]
                ]
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
                "agent": "phone_extractor",
                "execution_time": execution_time,
                "tools_used": [],
                "warnings": []
            }
        }

        # MANDATORY: Update state
        state['results']['phone_extractor'] = result
        state['current_data'] = result['data']
        state['execution_path'].append('phone_extractor')

    except Exception as e:
        import traceback
        error_detail = {
            "agent": "phone_extractor",
            "error": str(e),
            "traceback": traceback.format_exc(),
            "timestamp": datetime.now().isoformat()
        }
        state['errors'].append(error_detail)

        state['results']['phone_extractor'] = {
            "status": "error",
            "data": None,
            "metadata": {
                "agent": "phone_extractor",
                "execution_time": 0,
                "error": str(e)
            }
        }

    return state