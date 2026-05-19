

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage
from typing import Any

async def getAiAnswer(system_prompt: str, human_prompt:str, available_options:list[str], question: str, llm: ChatGroq)->str|Any:
    prompt_template = ChatPromptTemplate.from_messages([
        SystemMessage(content=system_prompt),
        ("human", human_prompt)
    ])
            
    prompt = prompt_template.format_messages(
        options=available_options,
        question=question
    )
    raw_response = await llm.ainvoke(prompt)
    answer = raw_response.content.strip().replace("**", "")
    return answer