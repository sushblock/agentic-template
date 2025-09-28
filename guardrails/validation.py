import json
from typing import Any


class OutputValidationError(Exception):
    pass


def ensure_json(obj: str | dict) -> dict:
    if isinstance(obj, dict):
        return obj
    try:
        return json.loads(obj)
    except Exception as e:
        raise OutputValidationError(f"Invalid JSON: {e}")