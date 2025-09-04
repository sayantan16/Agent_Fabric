def calculate_median_agent(state):
    """
    Compute the median value from a list of numbers
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
        if input_data is not None:
            try:
                # Receive an input list of numbers in JSON format
                numbers = json.loads(input_data)
                
                # Validate the input to ensure it is a non-empty array of numeric values
                if not isinstance(numbers, list) or len(numbers) == 0 or not all(isinstance(num, (int, float)) for num in numbers):
                    raise ValueError("Input must be a non-empty list of numeric values")
                
                # Sort the list of numbers in ascending order
                numbers.sort()
                
                # Determine if the list length is odd or even
                length = len(numbers)
                if length % 2 == 0:
                    # If the list length is even, calculate the average of the two middle elements
                    median = (numbers[length // 2 - 1] + numbers[length // 2]) / 2
                else:
                    # If the list length is odd, select the middle element as the median
                    median = numbers[length // 2]
                
                # Format output
                processed_data = {"median": median}
            except ValueError as e:
                state['errors'].append({
                    "agent": "calculate_median",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })
                processed_data = {"error": str(e)}
        else:
            processed_data = {"error": "No input data provided"}
        
        # Calculate execution time
        execution_time = (datetime.now() - start_time).total_seconds()
        
        # MANDATORY: Standard output envelope
        result = {
            "status": "success",
            "data": processed_data,
            "metadata": {
                "agent": "calculate_median",
                "execution_time": execution_time,
                "tools_used": [],
                "warnings": []
            }
        }
        
        # MANDATORY: Update state
        state['results']['calculate_median'] = result
        state['current_data'] = result['data']
        state['execution_path'].append('calculate_median')
        
    except Exception as e:
        import traceback
        error_detail = {
            "agent": "calculate_median",
            "error": str(e),
            "traceback": traceback.format_exc(),
            "timestamp": datetime.now().isoformat()
        }
        state['errors'].append(error_detail)
        
        state['results']['calculate_median'] = {
            "status": "error",
            "data": None,
            "metadata": {
                "agent": "calculate_median",
                "execution_time": 0,
                "error": str(e)
            }
        }
    
    return state