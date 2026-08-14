import pdfplumber
import os

def extract_text_from_file(file_path):
    """Extracts text from a given file (currently supports PDF via pdfplumber)."""
    text = ""
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == '.pdf':
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return None
    else:
        # We can implement OCR later for images, 
        # or we could rely on Gemini's multimodal capabilities.
        return "IMAGE_FILE"
