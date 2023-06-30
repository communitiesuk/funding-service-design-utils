"""
Data models for authentication
"""
from dataclasses import dataclass
from os import getenv
from typing import List
from typing import Mapping

from sentry_sdk import set_user

from .utils import get_highest_role_map


@dataclass
class User:
    full_name: str
    email: str
    roles: List[str]
    highest_role_map: Mapping[str, str]

    @classmethod
    def set_with_token(cls, token_payload):
        full_name = token_payload.get("fullName")
        email = token_payload.get("email")
        roles = token_payload.get("roles")
        # Set user in Sentry
        if getenv("SENTRY_DSN"):
            set_user(
                {
                    "email": token_payload.get("email"),
                    "id": token_payload.get("accountId"),
                    "username": token_payload.get("fullName"),
                }
            )
        return cls(
            full_name=full_name,
            email=email,
            roles=roles,
            highest_role_map=get_highest_role_map(roles),
        )
