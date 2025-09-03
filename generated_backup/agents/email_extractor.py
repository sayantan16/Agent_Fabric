def email_extractor_agent(state):
    """Agent that extracts emails from text."""
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from generated.tools.extract_emails import extract_emails
    
    try:
        # Get input
        text = state.get('current_data', {}).get('text', '')
        
        # Use tool
        emails = extract_emails(text)
        
        # Format output
        result = {
            "status": "success",
            "data": {
                "emails": emails,
                "count": len(emails)
            },
            "metadata": {
                "agent": "email_extractor",
                "tools_used": ["extract_emails"],
                "execution_time": 0.1
            }
        }
        
        # Update state
        state['results']['email_extractor'] = result
        state['current_data'] = result['data']
        state['execution_path'].append('email_extractor')
        
    except Exception as e:
        state['errors'].append({
            "agent": "email_extractor",
            "error": str(e)
        })
    
    return state
