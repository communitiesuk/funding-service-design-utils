"""
Data models for authentication
"""
from dataclasses import dataclass
from typing import List


@dataclass
class User:
    full_name: str
    email: str
    roles: List[str]
    highest_role: str
