import pdfplumber
import re
from typing import Dict, List
import base64

class PDFProcessor:
    def __init__(self):
        pass

    def clean_text(self, text: str) -> str:
        """Clean extracted text by removing unwanted characters and normalizing spacing."""
        # Remove special characters and normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove header/footer patterns
        text = re.sub(r'Page \d+ of \d+', '', text)
        # Remove multiple newlines
        text = re.sub(r'\n\s*\n', '\n', text)
        # Remove unwanted Unicode characters
        text = re.sub(r'[^\x00-\x7F]+', '', text)
        return text.strip()

    def extract_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF while maintaining structure."""
        full_text = []
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        cleaned_text = self.clean_text(text)
                        full_text.append(cleaned_text)
        except Exception as e:
            raise Exception(f"Error extracting PDF: {str(e)}")
        
        return '\n'.join(full_text)

    def get_base64_pdf(self, pdf_path: str) -> str:
        """Convert PDF to base64 string for API requests."""
        try:
            with open(pdf_path, "rb") as pdf_file:
                return base64.b64encode(pdf_file.read()).decode('utf-8')
        except Exception as e:
            raise Exception(f"Error converting PDF to base64: {str(e)}")