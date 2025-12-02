from pdf2image import convert_from_path
from PIL import Image
import pytesseract
from PyPDF2 import PdfReader
import io
import os
from google.cloud import vision

# Optional: Google Vision credentials
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/credentials.json"

def extract_text_from_pdf(pdf_path):
    text = ""

    # Try direct PDF text extraction first
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except:
        pass

    # If no text extracted, fallback to OCR
    if not text.strip():
        # Convert PDF to images
        images = convert_from_path(pdf_path)
        for img in images:
            # Google Vision OCR preferred
            try:
                client = vision.ImageAnnotatorClient()
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='PNG')
                image = vision.Image(content=img_byte_arr.getvalue())
                response = client.text_detection(image=image)
                for annotation in response.text_annotations:
                    text += annotation.description + "\n"
            except:
                # Fallback to pytesseract
                text += pytesseract.image_to_string(img, lang='guj') + "\n"

    return text