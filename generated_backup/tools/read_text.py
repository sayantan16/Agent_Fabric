def read_text(file_path):
    """Read plain text file."""
    import os

    if not os.path.exists(file_path):
        return {
            "error": f"File not found: {file_path}",
            "text": "",
            "status": "error",  # Added this line
        }

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

        return {
            "text": text,
            "lines": len(text.splitlines()),
            "chars": len(text),
            "status": "success",
            "file_path": file_path,
        }

    except Exception as e:
        return {"error": str(e), "text": "", "status": "error"}
