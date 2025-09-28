import httpx
from typing import List, Dict


class VLLMProvider:
    def __init__(self, model_name: str, base_url: str):
        self.model = model_name
        self.base_url = base_url.rstrip("/")


    def _post(self, path: str, payload: dict) -> dict:
        url = f"{self.base_url}/{path.lstrip('/')}"
        with httpx.Client(timeout=60) as client:
            r = client.post(url, json=payload)
            r.raise_for_status()
            return r.json()


    def complete(self, prompt: str, **kwargs) -> str:
        data = self._post("completions", {"model": self.model, "prompt": prompt, "max_tokens": 512})
        return data.get("choices", [{}])[0].get("text", "")


    def chat(self, messages: List[Dict], **kwargs) -> str:
        data = self._post("chat/completions", {"model": self.model, "messages": messages, "max_tokens": 512})
        return data.get("choices", [{}])[0].get("message", {}).get("content", "")