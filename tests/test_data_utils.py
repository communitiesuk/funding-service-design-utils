# flake8: noqa: E501
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
    "format_data": {
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
                "trusts one \n      . 125\n      . 1 April 2023 to 31 March 2024\n      . Capital\n      . Yes",
                "\n     trust two \n      . 456\n      . 1 April 2024 to 31 March 2025\n      . Revenue\n"
                "      . No",
            ],
        },
        "single_value": {
            "input_data": {
                "bbd0ec2a-972f-4d06-bf93-bf24786c3859": "Sky builders",
                "ac8bbdfe-6a39-45b8-8c0a-6558148388d1": "trust builders",
            },
            "expected_response": [". Sky builders", "\n     . trust builders"],
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
            "expected_response": "* trusts one \n       . 125\n       . 1 April 2023 to 31 March 2024\n       . Capital\n       . Yes\n\n     * trust two \n       . 456\n       . 1 April 2024 to 31 March 2025\n       . Revenue\n       . No",  # noqa
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
            "expected_response": "* cost one \n       . 4444\n\n     * cost two \n       . 4455",
        },
        "dict_two_str_values": {
            "input_data": [
                {"CZZvN": "Name", "jhgvDjv": "Xose"},
            ],
            "expected_response": (". Name: Xose"),
        },
        "dict_int_value": {
            "input_data": [
                {"hGsUaZ": "Revenue Costs", "UyaAHw": 817},
            ],
            "expected_response": (". Revenue Costs: 817"),
        },
        "dict_none_values": {
            "input_data": [
                {
                    "JizgZP": 0,
                    "gLQlyJ": "This contribute £30000",
                    "kjuHtl": "1 April 2024 to 31 March 2025",
                }
            ],
            "expected_response": "This contribute £30000 \n      . 0\n      . 1 April 2024 to 31 March 2025",
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
                        },
                        {
                            "key": "NxVqXd",
                            "title": "What funding are you applying?",
                            "type": "list",
                            "answer": "capital",
                        },
                        {
                            "key": "tZoOKx",
                            "title": "Partner organisation details",
                            "type": "multiInput",
                            "answer": [
                                {
                                    "GpLJDu": "version1",
                                    "IXjMWp": {
                                        "addressLine1": "La la land",
                                        "addressLine2": "",
                                        "town": "Mars",
                                        "county": "",
                                        "postcode": "XA15 1AX",
                                    },
                                    "MKbOlA": "https://www.wikipedia.org/",
                                    "OghGGr": None,
                                    "RphKTp": None,
                                }
                            ],
                        },
                        {
                            "key": "tZoOKL",
                            "title": "Partner's Job",
                            "type": "multiInput",
                            "answer": [
                                {
                                    "GpLJDu": "version2",
                                    "IXjMWp": {
                                        "addressLine1": "La la la land",
                                        "addressLine2": "",
                                        "town": "Moon",
                                        "county": "",
                                        "postcode": "XA15 1AL",
                                    },
                                }
                            ],
                        },
                        {
                            "key": "NxSxCd",
                            "title": "Do you want to mark this section as complete?",
                            "type": "boolean",
                            "answer": "markAsComplete",
                        },
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
                            "answer": "This-is-a-type-text-answer",
                            "key": "SRWtfV",
                            "title": "Testing hyphen in field type text",
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
                        {
                            "key": "NENGMj",
                            "title": "Which membership organisations are you a member of?",
                            "type": "list",
                            "answer": "homeless-link",
                        },
                        {
                            "key": "bCXNtj",
                            "title": "When did you start providing day provision?",
                            "type": "monthYear",
                            "answer": "2023-03",
                        },
                    ],
                    "question": "How much funding are you applying for?",
                },
                {
                    "fields": [
                        {
                            "answer": [
                                {
                                    "dpDFgB": "Test Funding Required NS Form",
                                    "iZdZrr": 40,
                                    "leIxEX": "1 April 2023 to 31 March 2024",
                                    "TrTaZQ": "None",
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
                        },
                        {
                            "key": "SxkwhF",
                            "type": "list",
                            "title": "Does your organisation have any alternative names?",
                            "answer": True,
                        },
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
            "What funding are you applying for?": "Both revenue and capital",
            "What funding are you applying?": "Capital",
            "Partner organisation details": "version1 \n      . La la land, Mars, XA15 1AX\n      . https://www.wikipedia.org/\n      . Not provided\n      . Not provided",  # noqa
            "Partner's Job": ". version2: La la la land, Moon, XA15 1AL",
            "Both revenue and capital": "4020",
            "Testing hyphen in field type text": "This-is-a-type-text-answer",
            "Revenue for 1 April 2024 to 31 March 2025": "4020",
            "Capital for 1 April 2023 to 31 March 2024": "1230",
            "Capital for 1 April 2024 to 31 March 2025": "1230",
            "Which membership organisations are you a member of?": "Homeless link",
            "When did you start providing day provision?": "March 2023",
            "Revenue costs": "Test Funding Required NS Form \n      . 40\n      . 1 April 2023 to 31 March 2024\n      . Not provided",  # noqa
            "Capital costs": "Test Funding Required NS Form \n      . 50\n      . 1 April 2024 to 31 March 2025",
            "Does your organisation have any alternative names?": "Yes",
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

test_data_sort_questions_answers_welsh = {
    "forms": [
        {
            "name": "test_form",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "SxkwhF",
                            "type": "list",
                            "title": "Os ydych yn llwyddiannus, a wnewch chi ddefnyddio eich cyllid o fewn y 12 mis nesaf?",
                            "answer": True,
                        },
                        {
                            "key": "SxkwhF",
                            "type": "list",
                            "title": "A ydych wedi sicrhau unrhyw gyllid cydweddu eto?",
                            "answer": False,
                        },
                    ],
                    "question": "Capital funding",
                },
            ],
        }
    ],
    "questions_answers": {
        "test_form": {
            "Os ydych yn llwyddiannus, a wnewch chi ddefnyddio eich cyllid o fewn y 12 mis nesaf?": "Oes",
            "A ydych wedi sicrhau unrhyw gyllid cydweddu eto?": "Nac Oes",
        }
    },
}


iso_and_nested_data = {
    "input_data": [
        {"HpLJyL__month": 3, "HpLJyL__year": 2022},
        {
            "addressLine1": "test",
            "addressLine2": "",
            "county": "",
            "postcode": "te3 2nr",
            "town": "test",
        },
        "wwww.example.com",
        None,
        None,
    ],
    "expected_response": "March 2022, test te3 2nr test, wwww.example.com",
}
