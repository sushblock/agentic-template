from ops.config.settings import settings
from models.providers.openai_provider import OpenAIProvider
from models.providers.anthropic_provider import AnthropicProvider
from models.providers.ollama_provider import OllamaProvider
from models.providers.vllm_provider import VLLMProvider


class LLM:
    def __init__(self, provider):
        self.provider = provider


    @classmethod
    def from_env(cls):
        provider_key = settings.model_provider.lower()
        if provider_key == "openai":
            return cls(OpenAIProvider(settings.model_name))
        if provider_key == "anthropic":
            return cls(AnthropicProvider(settings.model_name))
        if provider_key == "ollama":
            return cls(OllamaProvider(settings.model_name, settings.ollama_base_url))
        if provider_key == "vllm":
            return cls(VLLMProvider(settings.model_name, settings.vllm_base_url))
        raise ValueError(f"Unknown MODEL_PROVIDER: {settings.model_provider}")


    # Common interface
    def complete(self, prompt: str, **kwargs) -> str:
        return self.provider.complete(prompt, **kwargs)


    def chat(self, messages: list[dict], **kwargs) -> str:
        return self.provider.chat(messages, **kwargs)


    # Convenience patterns used in the graph
    def plan(self, goal: str, tools: list[str]) -> str:
        messages = [
            {"role": "system", "content": "You are a concise planner. Output numbered steps only."},
            {"role": "user", "content": f"Goal: {goal}\nTools: {', '.join(tools)}"},
        ]
        return self.chat(messages)


    def solve(self, goal: str, context: str) -> str:
        messages = [
            {"role": "system", "content": "Solve the task. Keep reasoning implicit, output final answer only."},
            {"role": "user", "content": f"Goal: {goal}\nContext:\n{context}"},
        ]
        return self.chat(messages)