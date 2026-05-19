import asyncio
import random
from playwright.async_api import Page, Locator

from app.utils.human import human_delay, human_typing, human_mouse_move
from langchain_groq import ChatGroq
from app.utils.bot_question import getNaukriBotQuestion
from app.bot.handle_options import getAvailableOptions
from app.ai.ai_answer import getAiAnswer
from typing import Any
from app.ai.rag.context import find_context_from_vector_db



async def handle_questionnaire(page: Page, llm: ChatGroq, system_prompt:str, human_prompt:str, vector_store: Any):
    if not llm:
        return

    try:
        chat_container = page.locator('.chatbot_MessageContainer')
        await chat_container.wait_for(state='visible', timeout=8000)
        print("🚨 JARVIS: Questionnaire detected! Analyzing...")
        
        while True:
            if not await chat_container.is_visible():
                print("✅ JARVIS: Questionnaire Closed.")
                break

            await asyncio.sleep(random.uniform(2.0, 3.5))

            question: str = await getNaukriBotQuestion(page)

            if question == None:
                continue
        
            context = find_context_from_vector_db(question, vector_store) if vector_store else ""
            
            current_system_prompt = system_prompt.replace("\\{context\\}", context).replace("{context}", context)
            
            input_box = page.locator('.textArea[contenteditable="true"]')
            is_text = await input_box.is_visible()
            available_options: list[str] = []

            if not is_text:
                available_options = await getAvailableOptions(chat_container)
                if available_options: print(f"🔘 Options detected: {available_options}")

            print("🧠 JARVIS: Thinking...")
            
            answer = await getAiAnswer(current_system_prompt, human_prompt, available_options, question, llm)
            
            print(f"✅ JARVIS Answer: {answer}")

            if is_text:
                await handleTextResponse(input_box, answer, page)

            elif available_options:
                await handleOptionResponse(available_options, answer, chat_container, page)
                
            

            # SUBMIT
            await clickSaveButton(page)

    except Exception as e:
        print(f"🤖 JARVIS Error in questionnaire: {repr(e)}")


async def handleTextResponse(input_box: Locator, answer: str, page: Page):
    try:
        await input_box.click()
        await page.keyboard.press('Control+A')
        await page.keyboard.press('Backspace')
        await human_typing(page.keyboard, answer)
        await human_delay(1, 2)
    except Exception as e:
        print(f"🤖 Error interacting with text box: {e}")

async def handleOptionResponse(available_options: list[str], answer:str|Any, chat_container: Locator, page: Page):
    try:
        if not isinstance(answer, str):
            answer = str(answer)
            
        matched = next((opt for opt in available_options if opt.lower() in answer.lower()), None)
        if matched:
            target = chat_container.get_by_text(matched, exact=True).last
            await human_mouse_move(page)
            await target.click(force=True)
            # Force check hidden radio button to enable 'Save'
            radio_id = await target.get_attribute("for")
            if radio_id:
                try: await page.locator(f"#{radio_id}").check(force=True)
                except: pass
        else:
            await chat_container.get_by_text(answer).last.click(force=True)
    except Exception as e:
        print(f"🤖 Error selecting option: {e}")

async def clickSaveButton(page: Page):
    try:
        # SUBMIT
        save_btn = page.locator('.send:not(.disabled) .sendMsg')
        if await save_btn.is_visible():
            await save_btn.click()
            print("👆 JARVIS: Clicked Save.")
            await human_delay(1, 2)
        else:
            await page.keyboard.press('Enter')
    except Exception as e:
        print(f"🤖 Error clicking save button: {e}")
    