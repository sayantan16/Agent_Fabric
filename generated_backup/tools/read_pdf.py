def read_pdf(file_path):
    """Extract text from PDF file using PyPDF2."""
    import PyPDF2
    import os

    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}", "text": ""}

    try:
        text_content = []

        with open(file_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)

            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                if text.strip():
                    text_content.append(text)

        full_text = "\n\n".join(text_content)

        return {
            "text": full_text,
            "pages": num_pages,
            "status": "success",
            "file_path": file_path,
        }

    except Exception as e:
        return {"error": str(e), "text": "", "status": "error"}
