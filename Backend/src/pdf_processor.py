import PyPDF2
from pdfminer.high_level import extract_text
from pdf2image import convert_from_path
import pytesseract
import pdfplumber
from PIL import Image


class PDFProcessor:
    @staticmethod
    def extract_text(pdf_path):
        # Extract text from PDF using pdfminer
        text_chunks = []
        text = extract_text(pdf_path)  # Extract text content from the PDF
        text_chunks.append({"text": text, "source": pdf_path})
        
        # Extract tables from PDF
        tables = PDFProcessor.extract_tables_from_pdf(pdf_path)
        for table in tables:
            text_chunks.append({"text": table, "source": pdf_path})

        # Extract images from PDF and use OCR to extract text
        image_text = PDFProcessor.extract_text_from_pdf_images(pdf_path)
        if image_text:
            text_chunks.append({"text": image_text, "source": pdf_path})

        return text_chunks

    @staticmethod
    def extract_tables_from_pdf(pdf_path):
        # Extract tables using pdfplumber
        table_chunks = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    # Convert table to Markdown-like format
                    table_chunks.append(
                        "\n".join([" | ".join(row) for row in table])
                    )
        return table_chunks

    @staticmethod
    def extract_text_from_pdf_images(pdf_path):
        # Convert PDF to images and extract text via OCR
        images = convert_from_path(pdf_path)
        image_texts = []
        for page_number, image in enumerate(images):
            text = pytesseract.image_to_string(image)
            if text.strip():
                image_texts.append(f"Page {page_number + 1}: {text.strip()}")
        return "\n".join(image_texts)  # Return all OCR text

    @staticmethod
    def extract_text_from_image(image_path):
        # OCR text extraction from image using Tesseract
        image = Image.open(image_path)
        return pytesseract.image_to_string(image)
