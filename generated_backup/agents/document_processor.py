def document_processor_agent(state):
    """Agent that processes text documents to extract key information."""
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from generated.tools.read_text import read_text
    from generated.tools.extract_emails import extract_emails
    from generated.tools.extract_urls import extract_urls
    from generated.tools.extract_numbers import extract_numbers
    
    try:
        # Initialize state components if missing
        if 'results' not in state:
            state['results'] = {}
        if 'errors' not in state:
            state['errors'] = []
        if 'execution_path' not in state:
            state['execution_path'] = []
        
        # Get input from state
        file_path = state.get('current_data', {}).get('file_path', '')
        
        # Read text from file
        text = read_text(file_path)
        
        # Extract entities from text
        emails = extract_emails(text)
        urls = extract_urls(text)
        numbers = extract_numbers(text)
        
        # Prepare result
        result = {
            "status": "success",
            "data": {
                "emails": emails,
                "urls": urls,
                "numbers": numbers
            },
            "metadata": {
                "agent": "document_processor",
                "tools_used": ["read_text", "extract_emails", "extract_urls", "extract_numbers"],
                "execution_time": 0.5
            }
        }
        
        # Update state
        state['results']['document_processor'] = result
        state['current_data'] = result['data']
        state['execution_path'].append('document_processor')
        
    except Exception as e:
        state['errors'].append({
            "agent": "document_processor",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        })
        
        # Still update results with error status
        state['results']['document_processor'] = {
            "status": "error",
            "data": None,
            "metadata": {
                "agent": "document_processor",
                "error": str(e)
            }
        }
    
    return state