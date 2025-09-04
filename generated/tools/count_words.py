def count_words(input_data=None):
    """
    Count the number of words in text input.

    Args:
        input_data: Any input type - will be handled gracefully.

    Returns:
        int: The number of words in the input data.
    """
    # MANDATORY: Handle None input
    if input_data is None:
        return 0

    # MANDATORY: Type flexibility
    try:
        # Handle different input types
        if isinstance(input_data, str):
            data = input_data
        elif isinstance(input_data, dict):
            # Extract from common keys
            data = None
            for key in ['text', 'data', 'value', 'content']:
                if key in input_data:
                    data = input_data[key]
                    break
            if data is None:
                data = str(input_data)
        elif isinstance(input_data, (list, tuple)):
            data = ' '.join(map(str, input_data))
        elif isinstance(input_data, (int, float)):
            data = str(input_data)
        else:
            # Convert to string as fallback
            try:
                data = str(input_data)
            except:
                return 0

        # TOOL LOGIC HERE
        # Process input data
        result = len(data.split())

        return result

    except Exception as e:
        # NEVER raise exceptions, always return default
        return 0