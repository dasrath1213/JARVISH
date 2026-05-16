from langchain_groq import ChatGroq


def init_llm():
    try:    
        # Using the massive 120B model for high-IQ reasoning
        local_llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.3)
        
        print("✅ JARVIS: AI Brain Online.")
        return local_llm
    except Exception as e:
        print(f"⚠️ AI Initialization Error: {str(e)}")
        return None