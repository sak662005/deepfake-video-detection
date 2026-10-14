from typing import Any


def create_access_token(subject: str) -> str:
    """TODO: create a signed JWT access token."""
    return f"token-for-{subject}"


def verify_token(token: str) -> dict[str, Any]:
    """TODO: verify a signed JWT access token."""
    return {"sub": "anonymous", "token": token}
