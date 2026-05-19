
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

def create_vector_db():
    try:
        DB_NAME="vector_db"
        EMBEDDING_MODEL_NAME="all-MiniLM-L6-v2"
        embedding=HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
        vector_store=Chroma(persist_directory=DB_NAME, embedding_function=embedding)
        return vector_store
        
    except Exception as e:
        print(f"Error while creating vector DB: {repr(e)}")
        return None
