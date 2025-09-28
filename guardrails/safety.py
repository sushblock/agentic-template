# Minimal safety checker (extend with real classifiers or external services)


DISALLOWED = ["weapon", "explosive", "harm"]


def is_safe(text: str) -> bool:
    t = (text or "").lower()
    return not any(bad in t for bad in DISALLOWED)