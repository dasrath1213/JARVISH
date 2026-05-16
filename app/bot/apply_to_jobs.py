from playwright.async_api import Page
import re
from langchain_groq import ChatGroq
from app.bot.handle_questions import handle_questionnaire
from app.utils.human import human_delay
from typing import Any

async def applyInBulk(page: Page, llm:ChatGroq, system_prompt:str, human_prompt:str, vector_store: Any):
    print(f"🤖 JARVIS: Applying to batch...")
    try:
        apply_btn = page.get_by_role("button", name=re.compile(r"^Apply", re.IGNORECASE))
        if await apply_btn.count() > 0:
            await apply_btn.first.click()
            await handle_questionnaire(page, llm, system_prompt, human_prompt, vector_store)
            print("🎉 JARVIS: Batch Operation Successful. Taking a short break before next batch.")
            await human_delay(1, 5)
    except Exception as e:
        print(f"🤖 JARVIS: Failed to apply in bulk. Error: {e}")
