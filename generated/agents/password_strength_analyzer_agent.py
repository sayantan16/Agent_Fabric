def password_strength_analyzer_agent(state):
    """
    Process password_strength_analyzer tasks
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

        # AGENT LOGIC: Process input_data using tools
        if input_data is not None:
            # Validate the input
            passwords = [p.strip() for p in input_data.split('\n') if p.strip()]

            # Compute password metrics and assess strength
            password_results = []
            for password in passwords:
                length = len(password)
                has_upper = any(char.isupper() for char in password)
                has_lower = any(char.islower() for char in password)
                has_digit = any(char.isdigit() for char in password)
                has_symbol = any(char in '!@#$%^&*()_+{}[]|;:"<>,.?/' for char in password)
                complexity = int(has_upper) + int(has_lower) + int(has_digit) + int(has_symbol)
                strength = 'Weak'
                if length >= 8 and complexity >= 3:
                    strength = 'Strong'
                elif length >= 6 and complexity >= 2:
                    strength = 'Moderate'

                password_result = {
                    'password': password,
                    'length': length,
                    'complexity': complexity,
                    'strength': strength
                }
                password_results.append(password_result)

            # Format the final output
            processed_data = {
                'passwords': password_results
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
                "agent": "password_strength_analyzer",
                "execution_time": execution_time,
                "tools_used": [],
                "warnings": []
            }
        }

        # MANDATORY: Update state
        state['results']['password_strength_analyzer'] = result
        state['current_data'] = result['data']
        state['execution_path'].append('password_strength_analyzer')

    except Exception as e:
        import traceback
        error_detail = {
            "agent": "password_strength_analyzer",
            "error": str(e),
            "traceback": traceback.format_exc(),
            "timestamp": datetime.now().isoformat()
        }
        state['errors'].append(error_detail)

        state['results']['password_strength_analyzer'] = {
            "status": "error",
            "data": None,
            "metadata": {
                "agent": "password_strength_analyzer",
                "execution_time": 0,
                "error": str(e)
            }
        }

    return state