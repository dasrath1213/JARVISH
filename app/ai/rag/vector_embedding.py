
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_chroma import Chroma
def vector_embedding( vector_store: Chroma,documents: list[Document]):
    if not documents:
        return
    try:
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        resume_docs = text_splitter.split_documents(documents)
        chunk_ids = [f"resume_chunk_{i}" for i in range(len(resume_docs))]
        vector_store.add_documents(resume_docs, ids=chunk_ids)
        
    except Exception as e:
        print(f"🤖 JARVIS Error in setting up vector store: {repr(e)}")
