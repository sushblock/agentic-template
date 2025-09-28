import re
from typing import Tuple


EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"\\b(?:\\+?\\d{1,3}[ -]?)?(?:\\d[ -]?){7,12}\\b")


def redact_pii(text: str) -> Tuple[str, dict]:
    red = EMAIL_RE.sub("[EMAIL]", text)
    red = PHONE_RE.sub("[PHONE]", red)
    return red, {"email": EMAIL_RE.findall(text), "phone": PHONE_RE.findall(text)}