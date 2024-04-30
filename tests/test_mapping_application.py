import pytest
from fsd_utils.mapping.application.application_utils import convert_bool_value
from fsd_utils.mapping.application.application_utils import format_answer
from fsd_utils.mapping.application.application_utils import format_checkbox
from fsd_utils.mapping.application.application_utils import format_date_month_year
from fsd_utils.mapping.application.application_utils import format_month_year
from fsd_utils.mapping.application.application_utils import format_radio_field
from fsd_utils.mapping.application.application_utils import simplify_title
from fsd_utils.mapping.application.free_text import FreeText
from fsd_utils.mapping.application.languages import CY
from fsd_utils.mapping.application.languages import EN
from fsd_utils.mapping.application.multi_input import MultiInput
from fsd_utils.mapping.application.multi_input_utils import ProcessTypes
from fsd_utils.mapping.application.qa_mapping import extract_questions_and_answers
from tests.test_data_utils import multi_input_test_data
from tests.test_data_utils import test_data_sort_questions_answers
from tests.test_data_utils import test_data_sort_questions_answers_welsh


@pytest.mark.parametrize(
    "input_data, language, expected_response",
    [
        (True, "en", "Yes"),
        (True, None, "Yes"),
        (True, "", "Yes"),
        (True, "cy", "Oes"),
        (False, "en", "No"),
        (False, None, "No"),
        (False, "", "No"),
        (False, "cy", "Nac Oes"),
        (["address", True], "en", ["address", "Yes"]),
        (["address", True], None, ["address", "Yes"]),
        (["address", True], "", ["address", "Yes"]),
        (["address", True], "cy", ["address", "Oes"]),
        (["address", False], "en", ["address", "No"]),
        (["address", False], None, ["address", "No"]),
        (["address", False], "", ["address", "No"]),
        (["address", False], "cy", ["address", "Nac Oes"]),
        (None, "en", "Not provided"),
        (None, None, "Not provided"),
        (None, "", "Not provided"),
        (None, "cy", "Heb ei ddarparu"),
        ([["name", True], "en", ["name", "Yes"]]),
        ([["name", True], None, ["name", "Yes"]]),
        ([["name", True], "", ["name", "Yes"]]),
        ([["name", True], "cy", ["name", "Oes"]]),
        ([["name", False], "en", ["name", "No"]]),
        ([["name", False], None, ["name", "No"]]),
        ([["name", False], "", ["name", "No"]]),
        ([["name", False], "cy", ["name", "Nac Oes"]]),
    ],
)
def test_convert_bool_values(input_data, expected_response, language):
    response = convert_bool_value(input_data, language)
    assert response == expected_response


@pytest.mark.parametrize(
    "input_data, expected_response",
    [
        ("null", ""),
        (None, "Not provided"),
        (
            "555 dummy road, null, beautiful town, optional county, UU8 8UU",
            "555 dummy road, beautiful town, optional county, UU8 8UU",
        ),
        ("https://example.com/test-the-link", "https://example.com/test-the-link"),
        (["four five six"], ["four five six"]),
        ("ten eleven twelve", "ten eleven twelve"),
        ({"title": ["one-two-three"]}, {"title": ["one-two-three"]}),
    ],
)
def test_format_answer(input_data, expected_response):
    response = format_answer(input_data, EN)
    assert response == expected_response


@pytest.mark.parametrize(
    "section_name, remove_text, expected_response",
    [
        (
            "organisation-type-cof-round",
            ["cof", "ns"],
            ["organisation", "type"],
        ),
        (
            "organisation-name-ns-round",
            ["cof", "ns"],
            ["organisation", "name"],
        ),
        (
            "organisation-name-dpi-round",
            ["cof", "dpi"],
            ["organisation", "name"],
        ),
        (
            "organisation-name-cyp",
            ["cof", "cyp"],
            ["organisation", "name"],
        ),
        (
            "total-expected-cost-hsra",
            ["cof", "cyp", "hsra"],
            ["total", "expected", "cost"],
        ),
        ("organisation-address", ["cof", "ns"], ["organisation", "address"]),
    ],
)
def test_simplify_title(section_name, remove_text, expected_response):
    response = simplify_title(section_name, remove_text)
    assert response == expected_response


@pytest.mark.parametrize(
    "input_value, expected_response",
    [
        ("<p> Hello world </p>", "Hello world"),
        ("<ul><li>Item 1</li><li>Item 2</li></ul>", ". Item 1\n     . Item 2"),
        (
            "<ol><li>Item 1</li><li>Item 2</li></ol>",
            "1. Item 1\n     2. Item 2",
        ),
        ("text without html tags", "text without html tags"),
        (None, None),
        (["one", "two"], ["one", "two"]),
        (True, True),
        ("https://my-website.com", "https://my-website.com"),
    ],
)
def test_remove_html_tags(input_value, expected_response):

    response = FreeText.remove_html_tags(input_value)
    assert response == expected_response


def test_extract_questions_and_answers(app_context):
    forms = test_data_sort_questions_answers["forms"]

    response = extract_questions_and_answers(forms)
    assert response == test_data_sort_questions_answers["questions_answers"]


def test_extract_questions_and_answers_welsh(app_context):
    forms = test_data_sort_questions_answers_welsh["forms"]

    response = extract_questions_and_answers(forms, CY)
    assert response == test_data_sort_questions_answers_welsh["questions_answers"]


def test_extract_questions_and_answers_fail(app_context):
    forms = test_data_sort_questions_answers["incorrect_form_data"]

    with pytest.raises(Exception) as exc:
        extract_questions_and_answers(forms)

    assert str(exc.value) == test_data_sort_questions_answers["exception_message"]


@pytest.mark.parametrize(
    "input_value, expected_response",
    [
        (
            [
                "health-interventions",
                "employment-support",
            ],
            ". Health interventions\n     . Employment support",
        ),
        (
            ["Survivors of domestic abuse", "ethnic minorities"],
            ". Survivors of domestic abuse\n     . Ethnic minorities",
        ),
        (
            ["gis (geographical-information-system)"],
            ". Gis (geographical information system)",
        ),
    ],
)
def test_format_checkbox(input_value, expected_response):

    response = format_checkbox(input_value)
    assert response == expected_response


@pytest.mark.parametrize(
    "input_value, expected_response",
    [
        ("health-interventions", "Health interventions"),
        ("https://my-website.com", "https://my-website.com"),
        (None, None),
        (True, True),
        (["test-list-answer"], ["test-list-answer"]),
        (
            "gis (geographical-information-system)",
            "Gis (geographical information system)",
        ),
        ("capital", "Capital"),
    ],
)
def test_format_radio_field(input_value, expected_response):

    response = format_radio_field(input_value)
    assert response == expected_response


@pytest.mark.parametrize(
    "input_value, expected_response",
    [
        ("2023-11", "November 2023"),
        ("11-2023", "November 2023"),
    ],
)
def test_format_month_year(input_value, expected_response):

    response = format_month_year(input_value)
    assert response == expected_response


@pytest.mark.parametrize(
    "input_value, expected_response",
    [
        ("2023-11-01", "01 November 2023"),
        ("2023-11-1", "01 November 2023"),
        ("01-11-2023", "01 November 2023"),
        ("1-11-2023", "01 November 2023"),
        ("2023-11-19", "19 November 2023"),
        ("2023-1-1", "01 January 2023"),
    ],
)
def test_format_date_month_year(input_value, expected_response):

    response = format_date_month_year(input_value)
    assert response == expected_response


class TestMultiInput:
    @pytest.mark.parametrize(
        "input_data, expected_response",
        [
            (
                multi_input_test_data["format_data"]["multiple_values"]["input_data"],
                multi_input_test_data["format_data"]["multiple_values"][
                    "expected_response"
                ],
            ),
            (
                multi_input_test_data["format_data"]["single_value"]["input_data"],
                multi_input_test_data["format_data"]["single_value"][
                    "expected_response"
                ],
            ),
        ],
    )
    def test_format_data(self, app_context, input_data, expected_response):
        response = MultiInput.format_data(input_data, EN)
        assert response == expected_response

    @pytest.mark.parametrize(
        "input_data, expected_response",
        [
            (
                multi_input_test_data["map_data"]["dict_two_str_values"]["input_data"],
                multi_input_test_data["map_data"]["dict_two_str_values"][
                    "expected_response"
                ],
            ),
            (
                multi_input_test_data["map_data"]["dict_int_value"]["input_data"],
                multi_input_test_data["map_data"]["dict_int_value"][
                    "expected_response"
                ],
            ),
            (
                multi_input_test_data["map_data"]["dict_none_values"]["input_data"],
                multi_input_test_data["map_data"]["dict_none_values"][
                    "expected_response"
                ],
            ),
        ],
    )
    def test_map_multi_input_data(self, app_context, input_data, expected_response):
        response = MultiInput.map_multi_input_data(input_data, EN)
        assert response == expected_response

    @pytest.mark.parametrize(
        "input_data, expected_response",
        [
            (
                {"hgYuhh": "Sky builders"},
                {"6ba7b810-9dad-11d1-80b4-00c04fd430c8": "Sky builders"},
            )
        ],
    )
    def test_str_single_item(
        self, app_context, input_data, expected_response, mock_uuid4
    ):
        response = ProcessTypes._str_single_item(input_data, sorted_data={})
        assert response == expected_response

    @pytest.mark.parametrize(
        "input_data, expected_response",
        [
            (
                {
                    "PrulfI": {"PrulfI__month": 6, "PrulfI__year": 2018},
                },
                {"date_6ba7b810-9dad-11d1-80b4-00c04fd430c8": "June 2018"},
            )
        ],
    )
    def test_dict_single_item(
        self, app_context, input_data, expected_response, mock_uuid4
    ):
        response = ProcessTypes._dict_single_item(input_data, sorted_data={})
        assert response == expected_response

    @pytest.mark.parametrize(
        "input_data, expected_response",
        [
            (
                {
                    "addressLine1": "123 Main St",
                    "addressLine2": "Apt 4B",
                    "county": "Example County",
                    "postcode": "12345",
                    "town": "Sample Town",
                    "extra_field": "This should be ignored",
                },
                "123 Main St, Apt 4B, Example County, 12345, Sample Town",
            )
        ],
    )
    def test_validate_address(
        self, app_context, input_data, expected_response, mock_uuid4
    ):
        response = ProcessTypes.validate_address(input_data)
        assert response == expected_response

    @pytest.mark.parametrize(
        "input_data, expected_response",
        [
            ({"key1": "Value One", "key2": "Value Two"}, ["Value One", "Value Two"]),
            (
                {
                    "HpLJDu": "Milestone one",
                    "LZbOBu": {"LZbOBu__month": 6, "LZbOBu__year": 2024},
                },
                ["Milestone one", "June 2024"],
            ),
        ],
    )
    def test_value_len_two(self, app_context, input_data, expected_response):
        response = ProcessTypes.value_len_two(input_data)
        assert response == expected_response

    @pytest.mark.parametrize(
        "input_data, expected_response",
        [
            (
                {"key1": "Value One", "key2": 42, "key3": "Value Three"},
                ([42, "Value Three"], "Value One"),
            ),
            (
                {
                    "gLqiyJ": "Capital title",
                    "yuzbjT": 200,
                    "HpLJyL": {"HpLJyL__month": 3, "HpLJyL__year": 2023},
                    "MadvIr": "Capital",
                },
                ((["March 2023", 200, "Capital"], "Capital title")),
            ),
        ],
    )
    def test_value_len_greater_two(self, app_context, input_data, expected_response):
        response = ProcessTypes.value_len_greater_two(input_data)
        assert response == expected_response

    @pytest.mark.parametrize(
        "input_data, expected_response",
        [
            (
                {"hjgthY__date": 11, "hjgthY__month": 2, "hjgthY__year": 2023},
                ("11 February 2023"),
            ),
        ],
    )
    def test_validated_iso_value(self, app_context, input_data, expected_response):
        response = ProcessTypes.validated_iso_value(input_data)
        assert response == expected_response

    @pytest.mark.parametrize(
        "input_data, expected_response",
        [
            (
                "date_6ba7b810-9dad-11d1-80b4-00c04fd430c8",
                True,
            ),
            (
                "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
                True,
            ),
            (
                "date_6ba7b810-9dad-11d1",
                False,
            ),
        ],
    )
    def test_is_valid_uuid(self, app_context, input_data, expected_response):
        response = ProcessTypes.is_valid_uuid(input_data)
        assert response == expected_response
