def csv_analyzer_agent(state):
    """Agent that analyzes CSV data to extract statistics and create summaries."""
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from generated.tools.read_csv import read_csv
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
        
        # Get CSV file path from state
        csv_file_path = state.get('current_data', {}).get('file_path', '')
        
        # Read CSV file using read_csv tool
        df = read_csv(csv_file_path)
        
        # Extract numeric data from columns
        numeric_columns = []
        numeric_data = {}
        for column in df.columns:
            try:
                numeric_data[column] = df[column].apply(extract_numbers).tolist()
                numeric_columns.append(column)
            except:
                pass
        
        # Calculate statistics for numeric columns
        column_stats = {}
        for column in numeric_columns:
            column_stats[column] = {
                "mean": calculate_mean(numeric_data[column]),
                "median": calculate_median(numeric_data[column])
            }
        
        # Create summary
        summary = {
            "row_count": len(df),
            "column_count": len(df.columns),
            "numeric_columns": numeric_columns,
            "column_statistics": column_stats
        }
        
        # Update state
        state['results']['csv_analyzer'] = {
            "status": "success",
            "data": summary
        }
        state['current_data'] = summary
        state['execution_path'].append('csv_analyzer')
        
    except Exception as e:
        state['errors'].append({
            "agent": "csv_analyzer",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        })
        
        # Still update results with error status
        state['results']['csv_analyzer'] = {
            "status": "error",
            "data": None,
            "metadata": {
                "agent": "csv_analyzer",
                "error": str(e)
            }
        }
    
    return state