def read_csv(input_data=None):
    """
    Read CSV file using pandas.
    Handles file path or dict with 'path' key.
    """
    import os
    import pandas as pd

    if input_data is None:
        return {"status": "error", "message": "No input provided", "data": []}

    try:
        # Extract file path
        if isinstance(input_data, str):
            file_path = input_data
        elif isinstance(input_data, dict):
            file_path = input_data.get("path", input_data.get("file_path", ""))
        else:
            return {"status": "error", "message": "Invalid input type", "data": []}

        if not file_path:
            return {"status": "error", "message": "No file path provided", "data": []}

        # Read CSV
        if not os.path.exists(file_path):
            return {
                "status": "error",
                "message": f"File not found: {file_path}",
                "data": [],
            }

        df = pd.read_csv(file_path)

        return {
            "status": "success",
            "data": df.to_dict("records"),
            "shape": {"rows": len(df), "columns": len(df.columns)},
            "columns": df.columns.tolist(),
            "preview": df.head(5).to_dict("records"),
        }

    except Exception as e:
        return {"status": "error", "message": str(e), "data": []}
