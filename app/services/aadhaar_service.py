import re

AADHAAR_PATTERN = r"\b\d{4}\s?\d{4}\s?\d{4}\b"


def extract_aadhaar(text: str) -> str | None:

    match = re.search(
        AADHAAR_PATTERN,
        text
    )

    if not match:
        return None

    return match.group().replace(" ", "")


def validate_aadhaar(aadhaar: str | None) -> bool:

    if aadhaar is None:
        return False

    if len(aadhaar) != 12:
        return False

    return aadhaar.isdigit()