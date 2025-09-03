def text_analyzer_agent(state):
    """Analyze text to extract emails and numbers."""
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from generated.tools.extract_emails import extract_emails
    from generated.tools.extract_numbers import extract_numbers
    
    try:
        # Initialize state components if missing
        if 'results' not in state:
            state['results'] = {}
        if 'errors' not in state:
            state['errors'] = []
        if 'execution_path' not in state:
            state['execution_path'] = []
        
        # Get text from state
        text = state.get('current_data', {}).get('text', '')
        
        # Extract emails and numbers
        emails = extract_emails(text)
        numbers = extract_numbers(text)
        
        # Combine results into output dictionary
        output = {
            'emails': emails,
            'numbers': numbers
        }
        
        # Update state
        state['results']['text_analyzer'] = {
            'status': 'success',
            'data': output,
            'metadata': {
                'agent': 'text_analyzer_agent',
                'tools_used': ['extract_emails', 'extract_numbers'],
                'execution_time': 0.5
            }
        }
        state['current_data'] = output
        state['execution_path'].append('text_analyzer_agent')
    
    except Exception as e:
        state['errors'].append({
            'agent': 'text_analyzer_agent',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        })
        
        state['results']['text_analyzer'] = {
            'status': 'error',
            'data': None,
            'metadata': {
                'agent': 'text_analyzer_agent',
                'error': str(e)
            }
        }
    
    return state