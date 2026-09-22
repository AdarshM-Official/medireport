import pdfplumber
import os
import logging

try:
    from paddleocr import PaddleOCR
except ImportError:
    PaddleOCR = None

try:
    import pydicom
except ImportError:
    pydicom = None

logger = logging.getLogger(__name__)

# Initialize PaddleOCR model globally so it's not reloaded on every call
ocr_model = None

def get_ocr_model():
    global ocr_model
    if ocr_model is None and PaddleOCR is not None:
        ocr_model = PaddleOCR(use_angle_cls=True, lang='en')
    return ocr_model

def extract_text_from_file(file_path):
    """Extracts text from a given file (supports PDF, Images via PaddleOCR, and DICOM metadata)."""
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
            logger.error(f"Error reading PDF: {e}")
            return None
            
    elif ext in ['.png', '.jpg', '.jpeg']:
        model = get_ocr_model()
        if not model:
            return "OCR is not available (PaddleOCR not installed)."
            
        try:
            result = model.ocr(file_path, cls=True)
            if result and result[0]:
                for line in result[0]:
                    extracted_text = line[1][0]
                    text += extracted_text + "\n"
            return text
        except Exception as e:
            logger.error(f"Error during OCR: {e}")
            return f"Error extracting text from image: {e}"
            
    elif ext == '.dcm':
        if not pydicom:
            return "DICOM support is not available (pydicom not installed)."
            
        try:
            dicom_data = pydicom.dcmread(file_path)
            
            # Extract relevant text metadata
            text += "DICOM Metadata Extracted:\n"
            
            # Helper to safely extract DICOM attributes
            def get_attr(data, attr_name):
                return str(getattr(data, attr_name, ''))
                
            fields_to_extract = [
                ('Patient Name', 'PatientName'),
                ('Patient ID', 'PatientID'),
                ('Patient Sex', 'PatientSex'),
                ('Patient Age', 'PatientAge'),
                ('Study Date', 'StudyDate'),
                ('Study Description', 'StudyDescription'),
                ('Series Description', 'SeriesDescription'),
                ('Modality', 'Modality'),
                ('Body Part Examined', 'BodyPartExamined'),
                ('Institution Name', 'InstitutionName'),
                ('Referring Physician Name', 'ReferringPhysicianName')
            ]
            
            for label, attr in fields_to_extract:
                val = get_attr(dicom_data, attr)
                if val:
                    text += f"{label}: {val}\n"
                    
            return text
        except Exception as e:
            logger.error(f"Error reading DICOM: {e}")
            return f"Error extracting text from DICOM: {e}"
    else:
        return f"Unsupported file type: {ext}"
