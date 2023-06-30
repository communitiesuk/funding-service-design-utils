from typing import Mapping

import jwt as jwt
from flask import current_app

from .config import config_var_rs256_public_key


def _validate_token(token, key, algorithms):
    return jwt.decode(token, key, algorithms=algorithms)


def validate_token_rs256(token):
    key = current_app.config.get(config_var_rs256_public_key)
    return _validate_token(token, key, algorithms=["RS256"])


_ROLE_HIERARCHY = [
    "LEAD_ASSESSOR",
    "ASSESSOR",
    "COMMENTER",
]


def get_highest_role_map(roles: list[str]) -> Mapping[str, str]:
    roles_with_fund_prefix = tuple(f"_{rh}" for rh in _ROLE_HIERARCHY)
    filtered_roles = [r for r in roles if r.endswith(roles_with_fund_prefix)]

    fund_short_name_to_roles_list = {}
    for role in filtered_roles:
        fund_short_name, sub_role = role.split("_", 1)
        if fund_short_name in fund_short_name_to_roles_list:
            fund_short_name_to_roles_list[fund_short_name].append(sub_role)
        else:
            fund_short_name_to_roles_list[fund_short_name] = [sub_role]

    fund_short_name_to_highest_role = {}
    for fund_short_name, roles_list in fund_short_name_to_roles_list.items():
        highest_role, *_ = sorted(roles_list, key=lambda x: _ROLE_HIERARCHY.index(x))
        fund_short_name_to_highest_role[fund_short_name] = highest_role

    return fund_short_name_to_highest_role
