def calculate_median(input_data=None):
        """
        Calculate median of numbers
        """
        
        if input_data is None:
            return {"status": "no_input", "result": None}
        
        try:
            result = {"status": "success"}
            
            # Process based on input type
            if isinstance(input_data, str):
                result["text_length"] = len(input_data)
                result["word_count"] = len(input_data.split())
                result["processed"] = input_data.strip()
            elif isinstance(input_data, dict):
                result["keys"] = list(input_data.keys())
                result["size"] = len(input_data)
                result["processed"] = input_data
            elif isinstance(input_data, list):
                result["count"] = len(input_data)
                result["processed"] = input_data
            else:
                result["type"] = type(input_data).__name__
                result["value"] = str(input_data)
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    