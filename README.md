# Agentic AI Template

A production-ready template for building AI agents with LangGraph, featuring multi-provider LLM support, built-in guardrails, and evaluation capabilities.

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Clone and install dependencies
git clone <your-repo>
cd agentic-template
pip install -r requirements.txt

# Create environment file
cp .env.example .env
```

### 2. Configure Your LLM Provider

Edit `.env` with your preferred provider:

```bash
# For OpenAI
MODEL_PROVIDER=openai
MODEL_NAME=gpt-4o-mini
OPENAI_API_KEY=your_key_here

# For Anthropic
MODEL_PROVIDER=anthropic
MODEL_NAME=claude-3-5-sonnet-20241022
ANTHROPIC_API_KEY=your_key_here

# For local Ollama (requires `ollama serve`)
MODEL_PROVIDER=ollama
MODEL_NAME=mistral:7b
OLLAMA_BASE_URL=http://localhost:11434

# For self-hosted VLLM
MODEL_PROVIDER=vllm
MODEL_NAME=your_model
VLLM_BASE_URL=http://localhost:8000/v1
```

### 3. Run the Agent

```bash
# CLI interface
python apps/cli/smoke.py --goal "Create a purchase order for 10 steel rods" --approve

# API server
python apps/api/main.py
# Then POST to http://localhost:8000/run
```

## 🏗️ Architecture Overview

This template implements a **4-stage agent workflow**:

```
Goal → Plan → Act → Validate → Commit
```

### Core Components

| Component | Purpose | Key Files |
|-----------|---------|-----------|
| **Agent Graph** | Main workflow orchestration | `agents/graphs/main_graph.py` |
| **State Management** | Typed state definitions | `agents/state.py` |
| **Guardrails** | Safety & PII protection | `agents/policies.py`, `guardrails/` |
| **LLM Adapter** | Multi-provider LLM interface | `models/llm_adapter.py` |
| **Domain Tools** | Business logic & external APIs | `tools/business/` |
| **RAG System** | Context retrieval | `rag/` |
| **Evaluation** | Testing & benchmarking | `evals/` |

## 📁 Project Structure

```
agentic-template/
├── agents/                    # Core agent logic
│   ├── graphs/main_graph.py  # LangGraph workflow definition
│   ├── policies.py           # Guardrails & safety checks
│   └── state.py              # State schema (TypedDict)
├── models/                    # LLM provider abstractions
│   ├── llm_adapter.py        # Unified LLM interface
│   └── providers/            # Provider implementations
│       ├── openai_provider.py
│       ├── anthropic_provider.py
│       ├── ollama_provider.py
│       └── vllm_provider.py
├── tools/                     # Domain tools & utilities
│   ├── business/             # Business logic tools
│   │   └── order_tool.py     # Example: purchase orders
│   └── common/               # Shared utilities
│       └── http.py           # HTTP client wrapper
├── guardrails/               # Safety & validation
│   ├── pii.py               # PII redaction
│   ├── safety.py            # Content safety
│   └── validation.py        # Output validation
├── rag/                      # Retrieval-Augmented Generation
│   ├── ingest.py            # Document ingestion
│   └── retriever.py         # Context retrieval
├── apps/                     # Application interfaces
│   ├── api/main.py          # FastAPI server
│   └── cli/smoke.py         # CLI interface
├── evals/                    # Evaluation framework
│   ├── datasets/            # Test datasets
│   └── runners/             # Evaluation runners
├── ops/                      # Operations & config
│   ├── config/settings.py   # Configuration management
│   └── observability/       # Logging & monitoring
└── tests/                    # Test suite
    └── test_smoke.py        # Smoke tests
```

## 🔄 How It Works

### 1. **Plan Stage**
- Takes user goal and available tools
- Generates numbered execution plan
- Uses LLM with system prompt for planning

### 2. **Act Stage**
- Executes the plan using domain tools
- Retrieves context via RAG system
- Generates draft output using LLM

### 3. **Validate Stage**
- Applies PII redaction to inputs/outputs
- Checks content safety
- Sets approval flags

### 4. **Commit Stage**
- Conditionally executes side effects
- Only runs if approved and safe
- Persists results to external systems

## 🛠️ Customization Guide

### Adding New Domain Tools

1. Create tool in `tools/business/`:
```python
# tools/business/my_tool.py
def my_domain_function(input_data: str) -> str:
    # Your business logic here
    return processed_result
```

2. Import in `agents/graphs/main_graph.py`:
```python
from tools.business.my_tool import my_domain_function

def act(state: AppState):
    result = my_domain_function(state["goal"])
    return {**state, "result": result}
```

### Adding New LLM Providers

1. Create provider in `models/providers/`:
```python
# models/providers/my_provider.py
class MyProvider:
    def __init__(self, model_name: str, **kwargs):
        # Initialize your provider
        pass
    
    def complete(self, prompt: str, **kwargs) -> str:
        # Implement completion logic
        pass
    
    def chat(self, messages: list[dict], **kwargs) -> str:
        # Implement chat logic
        pass
```

2. Add to `models/llm_adapter.py`:
```python
from models.providers.my_provider import MyProvider

@classmethod
def from_env(cls):
    # ... existing code ...
    if provider_key == "my_provider":
        return cls(MyProvider(settings.model_name))
```

### Enhancing Guardrails

1. **PII Protection**: Update `guardrails/pii.py` with new patterns
2. **Safety Checks**: Extend `guardrails/safety.py` with your rules
3. **Custom Validation**: Add validators in `guardrails/validation.py`

### RAG Integration

1. **Document Ingestion**: Implement `rag/ingest.py` with your vector store
2. **Context Retrieval**: Update `rag/retriever.py` with vector search
3. **Use in Graph**: Call `retrieve()` in the `act` stage

## 🧪 Testing & Evaluation

### Run Tests
```bash
# Smoke test
python -m pytest tests/test_smoke.py

# Full evaluation
python evals/datasets/runners/offline_eval.py
```

### Add Test Cases
Edit `evals/datasets/sample_tasks.json`:
```json
[
  {
    "goal": "Your test goal here",
    "approve": true,
    "expected_output": "Expected result"
  }
]
```

## 🚀 Deployment

### API Server
```bash
# Development
python apps/api/main.py

# Local
uvicorn apps.api.main:app --reload --port 8000

# Production with uvicorn
uvicorn apps.api.main:app --host 0.0.0.0 --port 8000
```

### Environment Variables
```bash
# Required
MODEL_PROVIDER=openai
MODEL_NAME=gpt-4o-mini
OPENAI_API_KEY=your_key

# Optional
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=my-agent
LOG_LEVEL=INFO
```

## 🔧 Configuration

All settings are in `ops/config/settings.py`. Key options:

- `model_provider`: LLM provider to use
- `model_name`: Specific model name
- `langchain_tracing_v2`: Enable LangSmith tracing
- `log_level`: Logging verbosity
- `app_env`: Environment (dev/prod)

## 📊 Monitoring

- **Structured Logging**: Uses `structlog` for JSON logs
- **LangSmith Tracing**: Built-in tracing for debugging
- **Health Checks**: `/health` endpoint for monitoring

## 🎯 Next Steps

1. **Add Domain Tools**: Replace `order_tool.py` with your business logic
2. **Implement RAG**: Connect to your vector store
3. **Enhance Guardrails**: Add domain-specific safety rules
4. **Add Evaluation**: Create test datasets for your use cases
5. **Scale**: Add human-in-the-loop checkpoints and retries

## 🤝 Contributing

1. Add new tools in `tools/business/`
2. Extend guardrails in `guardrails/`
3. Add tests in `tests/`
4. Update evaluation datasets in `evals/datasets/`

## 📚 Dependencies

- **LangGraph**: Workflow orchestration
- **LangChain**: LLM abstractions
- **FastAPI**: API server
- **Pydantic**: Data validation
- **Structlog**: Structured logging
- **ChromaDB**: Vector storage (optional)

See `requirements.txt` for complete list.
```