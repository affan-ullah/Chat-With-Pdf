README.md
markdown
Copy code
# PDF and Image Querying System

This project provides an API for uploading PDF and image files, extracting content, and enabling users to ask questions based on the uploaded files. The system uses OCR (Tesseract), table extraction (Camelot), and the Cohere API for generating responses.

## Features

- Upload multiple PDF and image files for processing.
- Extract text from PDFs, including images using OCR and tables.
- Store embeddings from text extraction in a vector database.
- Allow users to query the extracted data using natural language.
- Compare fields across multiple documents.
- Generate structured responses based on queries using the Cohere API.

## Prerequisites

Make sure the following are installed:

- Python 3.7+
- Tesseract OCR (for text extraction from images)
  - Install from [Tesseract GitHub](https://github.com/tesseract-ocr/tesseract) or using your package manager (e.g., `apt-get install tesseract-ocr`).
- Cohere API key (for response generation).

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-repo-url.git
   cd your-repo-directory
Create and activate a virtual environment (optional but recommended):

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
Install the dependencies:

bash
Copy code
pip install -r requirements.txt
Set up the configuration file (config.py) with your Cohere API key and Tesseract OCR path:

Set the COHERE_API_KEY in config.py.
Set the correct path for Tesseract OCR in TESSERACT_PATH.
Usage
Backend
Start the backend Flask application:

bash
Copy code
python app.py
The backend will run on http://127.0.0.1:5000/ by default.

Frontend
Open index.html in your browser to interact with the system.

Upload multiple PDF or image files using the upload form.

After files are uploaded, enter your query into the "Ask a Question" section and click Submit Query to get a response.

Endpoints
POST /ingest: Upload files (PDF, images) and extract their content (text, tables, OCR).
POST /query: Submit a query based on the uploaded files and retrieve a response.
POST /compare: Compare fields from multiple files.
Configuration
Make sure to configure the following in config.py:

FILE_DIRECTORY: Path where uploaded files are saved.
VECTOR_DB_PATH: Path where the vector database (FAISS index) will be stored.
COHERE_API_KEY: Your Cohere API key for response generation.
TESSERACT_PATH: The path to the Tesseract OCR binary if it's installed in a custom location.
License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
Flask for creating the backend API.
Cohere for providing LLM-based text generation.
Tesseract OCR for text extraction from images.
Camelot for table extraction from PDFs.
FAISS for vector similarity search.
markdown
Copy code

### Key Sections:

1. **Features**: Lists the main functionality of the application.
2. **Prerequisites**: Mentions the necessary software and dependencies.
3. **Installation**: Steps to set up the project and install dependencies.
4. **Usage**: Describes how to start the server, use the frontend, and interact with the API.
5. **Endpoints**: Provides an overview of the available API routes.
6. **Configuration**: Explains how to configure the `config.py` file.
7. **License and Acknowledgments**: Credits for the libraries used in the project.

This `README.md` will guide users through the setup and usage of your project. Make sure to replace placeholders like `your-repo-url` with the actual repository URL if you plan to share it publicly.





