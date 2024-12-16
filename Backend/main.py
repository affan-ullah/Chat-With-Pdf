import os
import numpy as np
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from src.pdf_processor import PDFProcessor
from src.embedding_service import EmbeddingService
from src.vector_store import VectorStore
from config import Config
import cohere  # Import the Cohere library
from flask_cors import CORS
import pytesseract
from PIL import Image
from pdf2image import convert_from_path  # To extract images from PDF
import pdfplumber  # For table extraction

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB limit
CORS(app)

# Initialize services
embedding_service = EmbeddingService()
vector_store = VectorStore(Config.VECTOR_DB_PATH)

# Initialize Cohere API key
co = cohere.Client(Config.COHERE_API_KEY)

# Ensure the file directory exists
if not os.path.exists(Config.FILE_DIRECTORY):
    os.makedirs(Config.FILE_DIRECTORY)

@app.route('/ingest', methods=['POST'])
def ingest_files():
    try:
        files = request.files.getlist('files')  # Retrieve multiple files from frontend
        if not files:
            return jsonify({'error': 'No files uploaded'}), 400

        all_chunks = []
        for file in files:
            save_path = os.path.join(Config.FILE_DIRECTORY, secure_filename(file.filename))  # Safe filename
            file.save(save_path)  # Save uploaded files

            # Process PDF files for text extraction
            if file.filename.lower().endswith('.pdf'):
                pdf_chunks = PDFProcessor.extract_text(save_path)
                all_chunks.extend(pdf_chunks)

                # Extract tables from PDF
                tables = extract_tables_from_pdf(save_path)
                for table in tables:
                    all_chunks.append({"text": table, "page": 1})

                # Extract images from the PDF and use OCR for text
                image_text = extract_text_from_pdf_images(save_path)
                if image_text:
                    all_chunks.append({"text": image_text, "page": 1})

            # Handle images (OCR text extraction)
            elif file.filename.lower().endswith(('.png', '.jpg', '.jpeg')): 
                image_text = extract_text_from_image(save_path)
                all_chunks.append({"text": image_text, "page": 1})

        # Proceed with embeddings if there are extracted chunks
        if all_chunks:
            texts = [chunk['text'] for chunk in all_chunks]
            embeddings = embedding_service.create_embeddings(texts)
            index = embedding_service.create_faiss_index(embeddings)
            vector_store.save_index(index, embeddings, all_chunks)
            return jsonify({'message': 'Files processed successfully'}), 200
        else:
            return jsonify({'message': 'No valid files found for processing'}), 200

    except Exception as e:
        print(f"Error: {str(e)}")  # Log error for debugging
        return jsonify({'error': str(e)}), 500

@app.route('/query', methods=['POST'])
def query_index():
    try:
        data = request.get_json()
        query = data.get('query')

        if not query:
            return jsonify({'error': 'Query parameter is missing'}), 400

        # Convert the query into embeddings
        query_embedding = embedding_service.create_embeddings([query])
        query_embedding = np.array(query_embedding, dtype='float32')

        # Load FAISS index and perform similarity search
        index, embeddings, metadata = vector_store.load_index()
        D, I = index.search(query_embedding, k=5)

        # Retrieve the top results
        results = [metadata[i] for i in I[0]]

        # Pass the retrieved chunks and query to the LLM to generate a response
        response = generate_llm_response(query, results)

        return jsonify({'response': response}), 200
    except Exception as e:
        print(f"Error: {str(e)}")  # Log error for debugging
        return jsonify({'error': str(e)}), 500

@app.route('/compare', methods=['POST'])
def compare_fields():
    try:
        # Receive the list of fields to compare
        data = request.get_json()
        fields = data.get('fields')  # List of field names to compare

        if not fields:
            return jsonify({'error': 'Fields parameter is missing'}), 400

        # Load the FAISS index, embeddings, and metadata
        index, embeddings, metadata = vector_store.load_index()

        comparison_results = {}
        for field in fields:
            # Use the field name as a query to find relevant chunks
            query_embedding = embedding_service.create_embeddings([field])
            query_embedding = np.array(query_embedding, dtype='float32')

            # Perform similarity search
            D, I = index.search(query_embedding, k=5)
            results = [metadata[i] for i in I[0]]

            # Store the results for the current field
            comparison_results[field] = results

        # Aggregate the results for comparison
        aggregated_data = aggregate_comparison_results(comparison_results)

        # Generate a structured response
        response = generate_structured_response(aggregated_data)

        return jsonify({'comparison': response}), 200

    except Exception as e:
        print(f"Error: {str(e)}")  # Log error for debugging
        return jsonify({'error': str(e)}), 500

def extract_text_from_image(image_path):
    # Extract text from an image using OCR (Tesseract)
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

def extract_text_from_pdf_images(pdf_path):
    # Extract images from the PDF and use OCR on each page
    images = convert_from_path(pdf_path)  # Convert each page of the PDF to an image
    image_texts = []
    for page_number, image in enumerate(images):
        image_text = pytesseract.image_to_string(image)
        if image_text.strip():  # If text was extracted
            image_texts.append(f"Page {page_number + 1}: {image_text.strip()}")
    return "\n".join(image_texts)  # Combine all extracted text from images

def extract_tables_from_pdf(pdf_path):
    # Extract tables from PDF using pdfplumber
    extracted_tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                # Convert table to Markdown-like format
                extracted_tables.append("\n".join([" | ".join(row) for row in table]))
    return extracted_tables

def generate_llm_response(query, results):
    # Prepare the context from the retrieved chunks
    context = "\n".join([result['text'] for result in results])

    # Construct the prompt with the context and the query
    prompt = f"""
    Given the following context:

    {context}

    Please answer the following question based on the above context:
    {query}
    """

    # Call the Cohere API to generate a response with the correct model
    try:
        response = co.generate(
            model='command-r-plus',  # Correct model ID
            prompt=prompt,
            max_tokens=500,
            temperature=0.2
        )
        return response.generations[0].text.strip()
    except Exception as e:
        return f"Error generating response: {str(e)}"

def aggregate_comparison_results(comparison_results):
    """Aggregate chunks for each field for structured comparison."""
    aggregated_data = []
    for field, results in comparison_results.items():
        for result in results:
            aggregated_data.append({
                "Field": field,
                "Chunk": result['text'],  # Add relevant chunk text
                "Source": result.get('source', 'Unknown')  # Add source metadata if available
            })
    return aggregated_data

def generate_structured_response(aggregated_data):
    """Generate a structured response in tabular or bullet-point format."""
    # Example: Generate a tabular response using markdown
    structured_response = "### Comparison Results:\n\n"
    structured_response += "| Field           | Chunk                         | Source         |\n"
    structured_response += "|-----------------|-------------------------------|----------------|\n"
    for entry in aggregated_data:
        field = entry["Field"]
        chunk = entry["Chunk"]
        source = entry["Source"]
        structured_response += f"| {field} | {chunk[:50]}... | {source} |\n"  # Limit chunk text for readability
    return structured_response

if __name__ == "__main__":
    app.run(debug=True)
