import os

class Config:
    # Directory to store uploaded files (PDFs, images, etc.)
    FILE_DIRECTORY = os.path.join(os.getcwd(), 'uploaded_files')

    # Path to the vector store (where the FAISS index and embeddings will be stored)
    VECTOR_DB_PATH = os.path.join(os.getcwd(), 'vector_db.index')

    # Cohere API key (for generating responses via Cohere API)
    COHERE_API_KEY = '<API Key>'  # replace <API Key> with actual api key.

    # Max file size for uploads (in bytes, 50MB in this case)
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB

    # Batch size for embeddings (number of text chunks to process in one batch)
    EMBEDDING_BATCH_SIZE = 32

    # Tesseract path for OCR processing (if Tesseract is installed at a custom location)
    TESSERACT_PATH = '/usr/local/bin/tesseract'  # Update to your Tesseract installation path

    # Logging configuration (optional, to help with debugging)
    LOGGING_ENABLED = True

    # Initialize app settings
    @staticmethod
    def init_app(app):
        # Any additional app initialization can go here
        app.config['FILE_DIRECTORY'] = Config.FILE_DIRECTORY
        app.config['VECTOR_DB_PATH'] = Config.VECTOR_DB_PATH
        app.config['COHERE_API_KEY'] = Config.COHERE_API_KEY
        app.config['MAX_CONTENT_LENGTH'] = Config.MAX_CONTENT_LENGTH
        app.config['EMBEDDING_BATCH_SIZE'] = Config.EMBEDDING_BATCH_SIZE
        app.config['TESSERACT_PATH'] = Config.TESSERACT_PATH
        app.config['LOGGING_ENABLED'] = Config.LOGGING_ENABLED

        # Ensure the necessary directories exist
        if not os.path.exists(Config.FILE_DIRECTORY):
            os.makedirs(Config.FILE_DIRECTORY)

        # Check if the vector database directory exists, and create it if not
        vector_db_dir = os.path.dirname(Config.VECTOR_DB_PATH)
        if not os.path.exists(vector_db_dir):
            os.makedirs(vector_db_dir)

