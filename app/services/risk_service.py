"""Fraud risk scoring service."""


def calculate_risk_score(
    aadhaar_valid: bool,
    pan_valid: bool,
    identity_found: bool,
    failed_attempts: int = 0,
) -> dict:
    """
    Calculate fraud risk score.

    Rules:
    - Invalid Aadhaar = +40
    - Invalid PAN = +40
    - Identity Not Found = +20
    - 3+ Failed Attempts = +30
    """

    score = 0

    if not aadhaar_valid:
        score += 40

    if not pan_valid:
        score += 40

    if not identity_found:
        score += 20

    if failed_attempts >= 3:
        score += 30

    score = min(score, 100)

    if score <= 30:
        level = "Low"

    elif score <= 70:
        level = "Medium"

    else:
        level = "High"

    return {
        "risk_score": score,
        "risk_level": level,
    }