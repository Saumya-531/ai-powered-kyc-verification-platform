import re

PAN_PATTERN = r"\b[A-Z]{5}[0-9]{4}[A-Z]\b"


def extract_pan(text: str) -> str | None:

    match = re.search(
        PAN_PATTERN,
        text
    )

    if not match:
        return None

    return match.group()


def validate_pan(pan: str | None) -> bool:

    if pan is None:
        return False

    return bool(
        re.fullmatch(
            PAN_PATTERN,
            pan
        )
    )