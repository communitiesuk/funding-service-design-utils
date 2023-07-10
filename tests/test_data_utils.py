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
                ". trusts one: [125, '1 April 2023 to 31 March 2024',"
                " 'Capital', 'Yes']",
                "     . trust two: [456, '1 April 2024 to 31 March 2025',"
                " 'Revenue', 'No']",
            ],
        },
        "single_value": {
            "input_data": {
                "bbd0ec2a-972f-4d06-bf93-bf24786c3859": "Sky builders",
                "ac8bbdfe-6a39-45b8-8c0a-6558148388d1": "trust builders",
            },
            "expected_response": [". Sky builders", "     . trust builders"],
        },
        "iso_values": {
            "input_data": {
                "Project one": [{"PrulfI__month": 1, "PrulfI__year": 2021}],
                "Project two": [{"PrulfI__month": 2, "PrulfI__year": 2022}],
            },
            "expected_response": (
                [
                    ". Project one: January 2021",
                    "     . Project two: February 2022",
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
                ". trusts one: [125, '1 April 2023 to 31 March 2024',"
                " 'Capital', 'Yes']\n     . trust two: [456, '1 April 2024 to"
                " 31 March 2025', 'Revenue', 'No']"
            ),
        },
        "single_value": {
            "input_data": [
                {"CZZYvE": "Sky builders"},
                {"CZZYvE": "trust builders"},
            ],
            "expected_response": ". Sky builders\n     . trust builders",
        },
        "integer_values": {
            "input_data": [
                {"GLQlOh": "cost one", "JtwkMy": 4444},
                {"GLQl6y": "cost two", "JtwkMt": 4455},
            ],
            "expected_response": ". cost one: 4444\n     . cost two: 4455",
        },
        "nested_dict_value_with_str_value": {
            "input_data": [
                {
                    "PrulfI": {"PrulfI__month": 2, "PrulfI__year": 2022},
                    "fFIuPP": "Milestone one",
                },
                {
                    "fFIuPP": "Milestone two",
                    "PrulfI": {
                        "PrulfI__date": 12,
                        "PrulfI__month": 3,
                        "PrulfI__year": 2023,
                    },
                },
            ],
            "expected_response": (
                ". Milestone one: February 2022\n     . Milestone" " two: 12 March 2023"
            ),
        },
    },
}


test_data_sort_questions_answers = {
    "forms": [
        {
            "name": "funding-required-ns",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": "both-revenue-and-capital",
                            "key": "NxVqXd",
                            "title": "What funding are you applying for?",
                            "type": "list",
                        }
                    ],
                    "question": "What funding are you applying for?",
                },
                {
                    "fields": [
                        {
                            "answer": "4020",
                            "key": "GRWtfV",
                            "title": "Both revenue and capital",
                            "type": "text",
                        },
                        {
                            "answer": "4020",
                            "key": "zvPzXN",
                            "title": "Revenue for 1 April 2024 to 31 March 2025",
                            "type": "text",
                        },
                        {
                            "answer": "1230",
                            "title": "Capital for 1 April 2023 to 31 March 2024",
                            "type": "text",
                        },
                        {
                            "answer": "1230",
                            "key": "pppiYl",
                            "title": "Capital for 1 April 2024 to 31 March 2025",
                            "type": "text",
                        },
                    ],
                    "question": "How much funding are you applying for?",
                },
                {
                    "fields": [
                        {
                            "answer": [
                                {
                                    "TrTaZQ": "Test Funding Required NS Form",
                                    "dpDFgB": "Test Funding Required NS Form",
                                    "iZdZrr": 40,
                                    "leIxEX": "1 April 2023 to 31 March 2024",
                                }
                            ],
                            "key": "mCbbyN",
                            "title": "Revenue costs",
                            "type": "multiInput",
                        }
                    ],
                    "question": "Revenue funding",
                },
                {
                    "fields": [
                        {
                            "answer": [
                                {
                                    "JtBjFp": 50,
                                    "cpFthG": "Test Funding Required NS Form",
                                    "mmwzGc": "1 April 2024 to 31 March 2025",
                                    "pMffVz": "Test Funding Required NS Form",
                                }
                            ],
                            "key": "XsAoTv",
                            "title": "Capital costs",
                            "type": "multiInput",
                        }
                    ],
                    "question": "Capital funding",
                },
            ],
        }
    ],
    "form_names": [
        "funding-required-ns",
    ],
    "questions_answers": {
        "funding-required-ns": {
            "What funding are you applying for?": "both-revenue-and-capital",
            "Both revenue and capital": "4020",
            "Revenue for 1 April 2024 to 31 March 2025": "4020",
            "Capital for 1 April 2023 to 31 March 2024": "1230",
            "Capital for 1 April 2024 to 31 March 2025": "1230",
            "Revenue costs": ". Test Funding Required NS Form: ['Test Funding Required NS Form', 40, '1 April 2023 to 31 March 2024']",  # noqa
            "Capital costs": ". 50: ['Test Funding Required NS Form', '1 April 2024 to 31 March 2025', 'Test Funding Required NS Form']",  # noqa
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
