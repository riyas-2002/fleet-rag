from langchain_community.document_loaders import PyPDFLoader, TextLoader
import os

def load_documents():
    documents = []

    # Load PDFs
    pdf_folder = "data/manuals"
    for file in os.listdir(pdf_folder):
        if file.endswith(".pdf"):
            path = os.path.join(pdf_folder, file)
            loader = PyPDFLoader(path)
            documents.extend(loader.load())

    # Load repair logs text
    log_path = "data/logs/repair_logs.txt"
    if os.path.exists(log_path):
        loader = TextLoader(log_path)
        documents.extend(loader.load())

    return documents