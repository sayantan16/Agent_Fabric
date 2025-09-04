def read_text(input_data=None):
    """
    Read text file and return contents.
    Handles file path or dict with 'path' key.
    """
    import os

    if input_data is None:
        return {"status": "error", "message": "No input provided", "content": ""}

    try:
        # Extract file path
        if isinstance(input_data, str):
            file_path = input_data
        elif isinstance(input_data, dict):
            file_path = input_data.get("path", input_data.get("file_path", ""))
        else:
            return {"status": "error", "message": "Invalid input type", "content": ""}

        if not file_path:
            return {
                "status": "error",
                "message": "No file path provided",
                "content": "",
            }

        # Read file
        if not os.path.exists(file_path):
            return {
                "status": "error",
                "message": f"File not found: {file_path}",
                "content": "",
            }

        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        return {
            "status": "success",
            "content": content,
            "lines": len(content.splitlines()),
            "chars": len(content),
        }

    except Exception as e:
        return {"status": "error", "message": str(e), "content": ""}
