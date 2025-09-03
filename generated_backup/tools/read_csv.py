def read_csv(file_path):
    """Read CSV file into structured data using pandas."""
    import pandas as pd
    import os

    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}", "data": None}

    try:
        df = pd.read_csv(file_path)

        return {
            "data": df.to_dict("records"),
            "columns": df.columns.tolist(),
            "shape": {"rows": len(df), "columns": len(df.columns)},
            "dtypes": df.dtypes.astype(str).to_dict(),
            "status": "success",
            "file_path": file_path,
        }

    except Exception as e:
        return {"error": str(e), "data": None, "status": "error"}
