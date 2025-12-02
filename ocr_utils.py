
import os, io
from google.cloud import vision_v1
from pdf2image import convert_from_path
from PIL import Image
import pytesseract

# GOOGLE_APPLICATION_CREDENTIALS setup
creds_json = os.environ.get("GOOGLE_CREDENTIALS_JSON")
if creds_json:
    path = "/tmp/gcloud_creds.json"
    with open(path, "w") as f:
        f.write(creds_json)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path

def image_to_text_with_vision(image_pil):
    client = vision_v1.ImageAnnotatorClient()
    buffered = io.BytesIO()
    image_pil.save(buffered, format="PNG")
    content = buffered.getvalue()
    image = vision_v1.Image(content=content)
    response = client.document_text_detection(image=image)
    return response.full_text_annotation.text

def pdf_page_images(pdf_path):
    return convert_from_path(pdf_path, dpi=300)

def extract_text_from_pdf(pdf_path):
    pages = pdf_page_images(pdf_path)
    all_text = []
    for page in pages:
        try:
            text = image_to_text_with_vision(page)
        except Exception:
            text = pytesseract.image_to_string(page, lang="guj+eng")
        all_text.append(text)
    return "\n\n".join(all_text)