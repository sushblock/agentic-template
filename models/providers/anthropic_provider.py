import os
from typing import List, Dict
from langchain_anthropic import ChatAnthropic


class AnthropicProvider:
    def __init__(self, model_name: str):
        if not os.getenv("ANTHROPIC_API_KEY"):
            raise RuntimeError("ANTHROPIC_API_KEY not set")
        self.llm = ChatAnthropic(model=model_name, temperature=0.2)


    def complete(self, prompt: str, **kwargs) -> str:
        return self.chat([{"role": "user", "content": prompt}], **kwargs)


    def chat(self, messages: List[Dict], **kwargs) -> str:
        result = self.llm.invoke(messages)
        return result.content