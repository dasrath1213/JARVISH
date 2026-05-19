

def find_context_from_vector_db(query: str, vector_store) -> str:
    if not vector_store:
        return ""
    
    try:
        retriver=vector_store.as_retriever(
        search_type="similarity", 
        search_kwargs={
        "k": 2      
        }
        )
        retrieved_docs=retriver.invoke(query)
        context = "\n".join([doc.page_content for doc in retrieved_docs])
        return context
    except Exception as e:
        print(f"Error while finding context from vector DB: {repr(e)}")
        return ""