"""
Data models for authentication
"""
from dataclasses import dataclass
from typing import List

from .utils import get_highest_role


@dataclass
class User:
    full_name: str
    email: str
    roles: List[str]
    highest_role: str

    @classmethod
    def set_with_token(cls, token_payload):
        full_name = token_payload.get("fullName")
        email = token_payload.get("email")
        roles = token_payload.get("roles")
        return cls(
            full_name=full_name,
            email=email,
            roles=roles,
            highest_role=get_highest_role(roles),
        )
