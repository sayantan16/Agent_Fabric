# Agent and Tool Creation Templates

## Tool Template Structure

Tools must be **pure functions** with these characteristics:
- No side effects (no file I/O, no API calls, no global state)
- Deterministic (same input always produces same output)
- Self-contained (all imports inside the function)
- Error handling (gracefully handle edge cases)
- Clear return types (consistent structure)

### Basic Tool Pattern
```python
def tool_name(input_param):
    """Clear description of what the tool does."""
    # Import statements inside function
    import required_module
    
    # Input validation
    if not input_param:
        return default_value
    
    # Core logic
    try:
        result = process(input_param)
        return result
    except Exception:
        return safe_default
Tool Categories

Extraction Tools - Extract specific data from text
Calculation Tools - Perform mathematical operations
Transformation Tools - Convert data formats
Validation Tools - Check data validity
Aggregation Tools - Combine or summarize data

Agent Template Structure
Agents coordinate tools and manage workflow state:
Basic Agent Pattern
pythondef agent_name(state):
    """Agent description."""
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from generated.tools.tool1 import tool1
    from generated.tools.tool2 import tool2
    
    try:
        # Initialize state if needed
        if 'results' not in state:
            state['results'] = {}
        if 'errors' not in state:
            state['errors'] = []
            
        # Get input data
        input_data = state.get('current_data', {})
        
        # Use tools
        result1 = tool1(input_data)
        result2 = tool2(result1)
        
        # Format output
        result = {
            "status": "success",
            "data": processed_data,
            "metadata": {
                "agent": "agent_name",
                "tools_used": ["tool1", "tool2"],
                "execution_time": 0.1
            }
        }
        
        # Update state
        state['results']['agent_name'] = result
        state['current_data'] = result['data']
        state['execution_path'].append('agent_name')
        
    except Exception as e:
        state['errors'].append({
            "agent": "agent_name",
            "error": str(e)
        })
        
    return state
Size Guidelines

Tools: 20-100 lines

Simple extractors: 20-40 lines
Complex processors: 40-80 lines
Multi-step validators: 60-100 lines


Agents: 50-300 lines

Single tool agents: 50-100 lines
Multi-tool coordinators: 100-200 lines
Complex workflow agents: 200-300 lines



Common Patterns
Data Extraction Pattern
pythondef extract_pattern(text):
    import re
    pattern = r'your_regex_here'
    matches = re.findall(pattern, text)
    return list(set(matches))  # Remove duplicates
Calculation Pattern
pythondef calculate_metric(data):
    if not data:
        return 0.0
    try:
        result = perform_calculation(data)
        return round(result, 2)
    except:
        return 0.0
State Update Pattern
python# In agent
state['results'][agent_name] = result
state['current_data'] = result['data']
state['execution_path'].append(agent_name)