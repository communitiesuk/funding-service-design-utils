from fsd_utils.authentication.utils import get_highest_role_map


def test_get_highest_role_map():
    roles = [
        "COF_ASSESSOR",  # highest role is assessor
        "COF_COMMENTER",
        "COF_SCOTLAND",
        "COF_ENGLAND",
        "COF_WALES",
        "COF_NORTHERNIRELAND",
        "NSTF_LEAD_ASSESSOR",  # highest role is lead assessor
        "NSTF_ASSESSOR",
        "NSTF_COMMENTER",
        "MOCKFUND_COMMENTER",  # highest role is commenter
        "INVALIDFUND_INVALIDROLE",  # invalid role is ignored
    ]

    result = get_highest_role_map(roles)

    assert "INVALIDFUND" not in result
    assert result == {
        "COF": "ASSESSOR",
        "NSTF": "LEAD_ASSESSOR",
        "MOCKFUND": "COMMENTER",
    }
