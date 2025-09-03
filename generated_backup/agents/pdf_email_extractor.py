def pdf_email_extractor_agent(state):
    """Agent that extracts email addresses from PDF documents."""
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from generated.tools.read_pdf import read_pdf
    from generated.tools.extract_emails import extract_emails
    
    import re
    
    try:
        # Initialize state components if missing
        if 'results' not in state:
            state['results'] = {}
        if 'errors' not in state:
            state['errors'] = []
        if 'execution_path' not in state:
            state['execution_path'] = []
        
        # Get PDF file path from state
        pdf_file_path = state.get('current_data', {}).get('pdf_file_path', '')
        
        # Read PDF content using read_pdf tool
        pdf_text = read_pdf(pdf_file_path)
        
        # Extract email addresses from the text
        emails = extract_emails(pdf_text)
        
        # Remove duplicates and format output
        unique_emails = list(set(emails))
        
        result = {
            "status": "success",
            "data": {
                "emails_found": len(unique_emails),
                "emails": unique_emails
            },
            "metadata": {
                "agent": "pdf_email_extractor",
                "tools_used": ["read_pdf", "extract_emails"],
                "execution_time": 0.5
            }
        }
        
        # Update state
        state['results']['pdf_email_extractor'] = result
        state['current_data'] = result['data']
        state['execution_path'].append('pdf_email_extractor')
    
    except Exception as e:
        state['errors'].append({
            "agent": "pdf_email_extractor",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        })
        
        # Still update results with error status
        state['results']['pdf_email_extractor'] = {
            "status": "error",
            "data": None,
            "metadata": {
                "agent": "pdf_email_extractor",
                "error": str(e)
            }
        }
    
    return state