
from app.config import prompts
import os

def get_system_prompt():
    return prompts.system_prompt


def get_human_prompt():
    return prompts.human_prompt
    