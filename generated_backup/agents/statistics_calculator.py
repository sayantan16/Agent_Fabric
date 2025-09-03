def statistics_calculator_agent(state):
    """Agent that calculates basic statistics from numbers in text."""
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from generated.tools.extract_numbers import extract_numbers
    from generated.tools.calculate_mean import calculate_mean
    from generated.tools.calculate_median import calculate_median
    
    try:
        # Initialize state components if missing
        if 'results' not in state:
            state['results'] = {}
        if 'errors' not in state:
            state['errors'] = []
        if 'execution_path' not in state:
            state['execution_path'] = []
            
        # Get input from state
        text = state.get('current_data', {}).get('text', '')
        
        # Use tools to extract and analyze numbers
        numbers = extract_numbers(text)
        
        if not numbers:
            result = {
                "status": "warning",
                "data": {
                    "message": "No numbers found in text",
                    "numbers_found": 0
                },
                "metadata": {
                    "agent": "statistics_calculator",
                    "tools_used": ["extract_numbers"],
                    "execution_time": 0.1
                }
            }
        else:
            # Calculate statistics using tools
            mean = calculate_mean(numbers)
            median = calculate_median(numbers)
            
            result = {
                "status": "success",
                "data": {
                    "numbers_found": len(numbers),
                    "numbers": numbers[:10],  # First 10 for preview
                    "statistics": {
                        "mean": round(mean, 2),
                        "median": median,
                        "min": min(numbers),
                        "max": max(numbers),
                        "sum": sum(numbers)
                    }
                },
                "metadata": {
                    "agent": "statistics_calculator",
                    "tools_used": ["extract_numbers", "calculate_mean", "calculate_median"],
                    "execution_time": 0.3
                }
            }
        
        # Update state
        state['results']['statistics_calculator'] = result
        state['current_data'] = result['data']
        state['execution_path'].append('statistics_calculator')
        
    except Exception as e:
        state['errors'].append({
            "agent": "statistics_calculator",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        })
        
        # Still update results with error status
        state['results']['statistics_calculator'] = {
            "status": "error",
            "data": None,
            "metadata": {
                "agent": "statistics_calculator",
                "error": str(e)
            }
        }
    
    return state