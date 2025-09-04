def read_json(input_data=None):
    """
    Read JSON file and parse contents.
    Handles file path or dict with 'path' key.
    """
    import os
    import json

    if input_data is None:
        return {"status": "error", "message": "No input provided", "data": {}}

    try:
        # Extract file path
        if isinstance(input_data, str):
            file_path = input_data
        elif isinstance(input_data, dict):
            file_path = input_data.get("path", input_data.get("file_path", ""))
        else:
            return {"status": "error", "message": "Invalid input type", "data": {}}

        if not file_path:
            return {"status": "error", "message": "No file path provided", "data": {}}

        # Read and parse JSON
        if not os.path.exists(file_path):
            return {
                "status": "error",
                "message": f"File not found: {file_path}",
                "data": {},
            }

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return {
            "status": "success",
            "data": data,
            "type": type(data).__name__,
            "keys": list(data.keys()) if isinstance(data, dict) else None,
        }

    except json.JSONDecodeError as e:
        return {"status": "error", "message": f"Invalid JSON: {str(e)}", "data": {}}
    except Exception as e:
        return {"status": "error", "message": str(e), "data": {}}
