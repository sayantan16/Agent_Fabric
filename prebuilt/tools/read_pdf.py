def read_pdf(input_data=None):
    """
    Read PDF file and extract text using PyPDF2.
    Handles file path or dict with 'path' key.
    """
    import os
    import PyPDF2

    if input_data is None:
        return {"status": "error", "message": "No input provided", "text": ""}

    try:
        # Extract file path
        if isinstance(input_data, str):
            file_path = input_data
        elif isinstance(input_data, dict):
            file_path = input_data.get("path", input_data.get("file_path", ""))
        else:
            return {"status": "error", "message": "Invalid input type", "text": ""}

        if not file_path:
            return {"status": "error", "message": "No file path provided", "text": ""}

        # Read PDF
        if not os.path.exists(file_path):
            return {
                "status": "error",
                "message": f"File not found: {file_path}",
                "text": "",
            }

        text = ""
        with open(file_path, "rb") as f:
            pdf_reader = PyPDF2.PdfReader(f)
            num_pages = len(pdf_reader.pages)

            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()

        return {
            "status": "success",
            "text": text,
            "pages": num_pages,
            "chars": len(text),
        }

    except Exception as e:
        return {"status": "error", "message": str(e), "text": ""}
