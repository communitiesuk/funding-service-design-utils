import pytest
from fsd_utils.simple_utils.data_utils import get_remote_data_as_json
from requests.exceptions import HTTPError


class TestDataUtils:
    def test_get_remote_data_json(self, flask_test_client):
        postcode = "SW1P 4DF"
        result = get_remote_data_as_json(f"https://postcodes.io/postcodes/{postcode}")
        assert postcode == result["result"]["postcode"]

    def test_get_remote_data_json_404(self, flask_test_client):
        with pytest.raises(HTTPError):
            get_remote_data_as_json("https://postcodes.io/postcodes/QQ11QQ")


multi_input_test_data = {
    "process_data": {
        "multiple_values": {
            "input_data": {
                "trusts one": [
                    125,
                    "1 April 2023 to 31 March 2024",
                    "Capital",
                    True,
                ],
                "trust two": [
                    456,
                    "1 April 2024 to 31 March 2025",
                    "Revenue",
                    False,
                ],
            },
            "expected_response": [
                "- trusts one: [125, '1 April 2023 to 31 March 2024',"
                " 'Capital', 'Yes']",
                "     - trust two: [456, '1 April 2024 to 31 March 2025',"
                " 'Revenue', 'No']",
            ],
        },
        "single_value": {
            "input_data": {
                "bbd0ec2a-972f-4d06-bf93-bf24786c3859": "Sky builders",
                "ac8bbdfe-6a39-45b8-8c0a-6558148388d1": "trust builders",
            },
            "expected_response": ["- Sky builders", "     - trust builders"],
        },
        "iso_values": {
            "input_data": {
                "Project one": [{"PrulfI__month": 1, "PrulfI__year": 2021}],
                "Project two": [{"PrulfI__month": 2, "PrulfI__year": 2022}],
            },
            "expected_response": (
                [
                    "- Project one: ['month: 1', 'year: 2021']",
                    "     - Project two: ['month: 2', 'year: 2022']",
                ]
            ),
        },
    },
    "map_data": {
        "multiple_values": {
            "input_data": [
                {
                    "AfAKxk": "trusts one",
                    "CrcLtW": 125,
                    "ndySbC": "1 April 2023 to 31 March 2024",
                    "pATWyM": "Capital",
                    "sIFBGc": True,
                },
                {
                    "AfAKxk": "trust two",
                    "CrcLtW": 456,
                    "ndySbC": "1 April 2024 to 31 March 2025",
                    "pATWyM": "Revenue",
                    "sIFBGc": False,
                },
            ],
            "expected_response": (
                "- trusts one: [125, '1 April 2023 to 31 March 2024',"
                " 'Capital', 'Yes']\n     - trust two: [456, '1 April 2024 to"
                " 31 March 2025', 'Revenue', 'No']"
            ),
        },
        "single_value": {
            "input_data": [
                {"CZZYvE": "Sky builders"},
                {"CZZYvE": "trust builders"},
            ],
            "expected_response": "- Sky builders\n     - trust builders",
        },
        "integer_values": {
            "input_data": [
                {"GLQlOh": "cost one", "JtwkMy": 4444},
                {"GLQl6y": "cost two", "JtwkMt": 4455},
            ],
            "expected_response": "- cost one: 4444\n     - cost two: 4455",
        },
        "nested_dict_value_with_str_value": {
            "input_data": [
                {
                    "PrulfI": {"PrulfI__month": 2, "PrulfI__year": 2022},
                    "fFIuPP": "Milestone one",
                },
                {
                    "fFIuPP": "Milestone two",
                    "PrulfI": {"PrulfI__month": 3, "PrulfI__year": 2023},
                },
            ],
            "expected_response": (
                "- Milestone one: ['month: 2', 'year: 2022']\n     - Milestone"
                " two: ['month: 3', 'year: 2023']"
            ),
        },
    },
}


test_data_sort_questions_answers = {
    "forms": [
        {
            "questions": [
                {
                    "category": "ZbxIUV",
                    "question": "Lead contact details",
                    "fields": [
                        {
                            "key": "fUMWcd",
                            "title": "Name of lead contact",
                            "type": "text",
                            "answer": "test name",
                        },
                        {
                            "key": "ayzqnK",
                            "title": (
                                "Is the lead contact the same person as the"
                                " authorised signatory?"
                            ),
                            "type": "list",
                            "answer": True,
                        },
                    ],
                }
            ],
            "name": "applicant-information-ns",
        },
    ],
    "form_names": [
        "objectives-and-activities-ns",
        "risk-and-deliverability-ns",
        "applicant-information-ns",
    ],
    "questions_answers": {
        "applicant-information-ns": {
            "Name of lead contact": "test name",
            "Is the lead contact the same person as the authorised signatory?": ("Yes"),
        }
    },
    "incorrect_form_data": [
        {
            "questions": [
                {
                    "category": "ZbxIUV",
                    "question": "Lead contact details",
                    "fields": [
                        {
                            "key": "fUMWcd",
                            "type": "text",
                            "answer": "test name",
                        },
                    ],
                }
            ],
            "name": "applicant-information-ns",
        },
    ],
    "exception_message": ("Could not map the data for form: applicant-information-ns"),
}
