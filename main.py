import asyncio
from app.ai.llm import init_llm
from app.ai.rag.create_vector_db import create_vector_db
from app.ai.rag.document_loader import document_loader
from app.ai.rag.vector_embedding import vector_embedding
from app.utils.file_loader import get_system_prompt, get_human_prompt
from app.bot.bot_runner import run_bot


async def main():
    print("🤖 JARVIS: Initializing Systems...")

    vector_store=create_vector_db()
    document=document_loader("data/resume.pdf")
    if vector_store and document:
        vector_embedding(vector_store, document)
    else:
        print("⚠️ JARVIS: Issue initializing vector store or document.")

    llm = init_llm()
    system_prompt = get_system_prompt()
    human_prompt = get_human_prompt()
    

    if llm is None:
        print("❌ JARVIS: AI Initialization Failed.")
        return
    
    if system_prompt is None or human_prompt is None:
        print("❌ JARVIS: Prompts Not Found.")
        return

    await run_bot(llm, system_prompt, human_prompt, vector_store)


if __name__ == "__main__":
    asyncio.run(main())