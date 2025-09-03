def read_json(file_path):
    """Parse JSON file into Python object."""
    import json
    import os

    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}", "data": None}

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        return {
            "data": data,
            "type": type(data).__name__,
            "status": "success",
            "file_path": file_path,
        }

    except Exception as e:
        return {"error": str(e), "data": None, "status": "error"}
