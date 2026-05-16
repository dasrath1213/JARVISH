
from langchain_community.document_loaders import PyPDFLoader
import os

def document_loader(file_path: str):
    try:
        if not os.path.exists(file_path):
            print(f"⚠️ JARVIS: File not found at {file_path}")
            return None
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        return documents
    except Exception as e:
        print(f"Error while loading document: {repr(e)}")
        return None