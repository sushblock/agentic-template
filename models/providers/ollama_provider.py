from typing import List, Dict
from ollama import Client


class OllamaProvider:
    def __init__(self, model_name: str, base_url: str):
        self.model = model_name
        self.client = Client(host=base_url)


    def complete(self, prompt: str, **kwargs) -> str:
        out = self.client.generate(model=self.model, prompt=prompt)
        return out.get("response", "")


    def chat(self, messages: List[Dict], **kwargs) -> str:
        # Convert to Ollama chat format
        out = self.client.chat(model=self.model, messages=messages)
        return out.get("message", {}).get("content", "")