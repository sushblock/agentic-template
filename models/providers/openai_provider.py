import os
from typing import List, Dict
from langchain_openai import ChatOpenAI


class OpenAIProvider:
    def __init__(self, model_name: str):
        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY not set")
        self.llm = ChatOpenAI(model=model_name, temperature=0.2)


    def complete(self, prompt: str, **kwargs) -> str:
        return self.chat([{"role": "user", "content": prompt}], **kwargs)


    def chat(self, messages: List[Dict], **kwargs) -> str:
        # messages: [{role, content}]
        result = self.llm.invoke(messages)
        return result.content