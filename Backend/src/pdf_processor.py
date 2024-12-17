import pdfplumber
from pdf2image import convert_from_path
import pytesseract
from pdfminer.high_level import extract_text
from PIL import Image


class PDFProcessor:
    @staticmethod
    def extract_text(pdf_path):
        """
        Extract text, tables, and OCR results from a PDF.

        Args:
            pdf_path (str): Path to the PDF file.

        Returns:
            list: A list of dictionaries containing text chunks and their source.
        """
        text_chunks = []

        # Extract text using pdfminer
        try:
            text = extract_text(pdf_path)
            if text and text.strip():
                text_chunks.append({"text": text.strip(), "source": pdf_path})
        except Exception as e:
            print(f"Error extracting text with pdfminer: {e}")

        # Extract tables using pdfplumber
        try:
            tables = PDFProcessor.extract_tables_from_pdf(pdf_path)
            for table in tables:
                if table.strip():  # Ensure the table is not empty
                    text_chunks.append({"text": table.strip(), "source": pdf_path})
        except Exception as e:
            print(f"Error extracting tables with pdfplumber: {e}")

        # Extract text from images using OCR
        try:
            image_text = PDFProcessor.extract_text_from_pdf_images(pdf_path)
            if image_text.strip():  # Ensure the OCR result is not empty
                text_chunks.append({"text": image_text.strip(), "source": pdf_path})
        except Exception as e:
            print(f"Error extracting text from images: {e}")

        return text_chunks

    @staticmethod
    def extract_tables_from_pdf(pdf_path):
        """
        Extract tables from a PDF using pdfplumber.

        Args:
            pdf_path (str): Path to the PDF file.

        Returns:
            list: A list of tables represented as Markdown-like strings.
        """
        table_chunks = []
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_number, page in enumerate(pdf.pages, start=1):
                    tables = page.extract_tables()
                    for table in tables:
                        if table:  # Ensure table is valid
                            # Clean up the table rows and cells
                            cleaned_table = []
                            for row in table:
                                if row:  # Ensure the row is not None
                                    # Replace None values in the row with empty strings
                                    cleaned_row = [str(cell) if cell is not None else "" for cell in row]
                                    cleaned_table.append(cleaned_row)
                            # Convert the cleaned table to a Markdown-like format
                            markdown_table = "\n".join([" | ".join(row) for row in cleaned_table])
                            table_chunks.append(f"Page {page_number}:\n{markdown_table}")
        except Exception as e:
            print(f"Error extracting tables with pdfplumber: {e}")
        return table_chunks

    @staticmethod
    def extract_text_from_pdf_images(pdf_path):
        """
        Extract text from PDF images using OCR.

        Args:
            pdf_path (str): Path to the PDF file.

        Returns:
            str: A concatenated string of OCR results from all images.
        """
        image_texts = []
        try:
            images = convert_from_path(pdf_path)
            for page_number, image in enumerate(images, start=1):
                text = pytesseract.image_to_string(image)
                if text and text.strip():  # Ensure valid OCR results
                    image_texts.append(f"Page {page_number}:\n{text.strip()}")
        except Exception as e:
            print(f"Error extracting text from PDF images: {e}")
        return "\n".join(image_texts)

    @staticmethod
    def extract_text_from_image(image_path):
        """
        Extract text from an image file using OCR.

        Args:
            image_path (str): Path to the image file.

        Returns:
            str: Extracted text from the image.
        """
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            return text.strip() if text else ""
        except Exception as e:
            print(f"Error extracting text from image: {e}")
            return ""
