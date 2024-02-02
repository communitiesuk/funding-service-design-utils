from enum import Enum
import pytest
from copy import deepcopy
from fsd_utils import evaluate_eoi_response, Eoi_Decision


TEST_SCHEMA_1 = {
    "aaa111": {
        "charity": {"result": Eoi_Decision.PASS, "caveat": None},
        "parish_council": {
            "result": Eoi_Decision.PASS,
            "caveat": None,
        },
        "plc": {
            "result": Eoi_Decision.FAIL,
            "caveat": None,
        },
    },
    "bbb222": {
        True: {"result": Eoi_Decision.PASS, "caveat": None},
        False: {"result": Eoi_Decision.FAIL, "caveat": None},
    },
    "ccc333": {
        10: {"result": Eoi_Decision.PASS, "caveat": None},
        15: {
            "result": Eoi_Decision.PASS_WITH_CAVEATS,
            "caveat": "Try not to cut down trees: This is a bit high",
        },
        20: {"result": Eoi_Decision.FAIL, "caveat": None},
    },
    "eee555": {
        "a": {"result": Eoi_Decision.PASS, "caveat": None},
        "b": {
            "result": Eoi_Decision.PASS_WITH_CAVEATS,
            "caveat": "Caveat heading: some caveat text",
        },
        "c": {"result": Eoi_Decision.FAIL, "caveat": None},
        #TODO need to add support for arbitrary comparison, eg. >, < etc - use eval() with f string to allow using the supplied operator from the schema
    },
}


TEST_EOI_FORMS_1 = [
    {
        "name": "test-form-1",
        "questions": [
            {
                "category": "GMkooI",
                "fields": [
                    {
                        "answer": "charity",
                        "key": "aaa111",
                        "title": "What type of org are you?",
                        "type": "text",
                    },
                    {
                        "answer": "something",
                        "key": "ddd444",
                        "title": "Question with no bearing on decision",
                        "type": "text",
                    },
                ],
                "question": "Test Question 1",
                "status": "COMPLETED",
            }
        ],
        "status": "COMPLETED",
    },
    {
        "name": "test-form-2",
        "questions": [
            {
                "category": "GMkooI",
                "fields": [
                    {
                        "answer": True,
                        "key": "bbb222",
                        "title": "Do you have a plan in place",
                        "type": "list",
                    },
                    {
                        "answer": 10,
                        "key": "ccc333",
                        "title": "How many trees will you have to cut down?",
                        "type": "list",
                    },
                ],
                "question": "Test Question 2",
                "status": "COMPLETED",
            },
            {
                "category": "GMkooI",
                "fields": [
                    {
                        "answer": "a",
                        "key": "eee555",
                        "title": "Another question with caveats",
                        "type": "list",
                    },
                    {
                        "answer": 200,
                        "key": "fff666",
                        "title": "Pass or fail based on number",
                        "type": "list",
                    },
                ],
            },
        ],
        "status": "COMPLETED",
    },
]


@pytest.mark.parametrize(
    "answers,schema,exp_result,exp_caveats",
    [
        (
            {"aaa111": "charity", "bbb222": True, "ccc333": 10},
            TEST_SCHEMA_1,
            Eoi_Decision.PASS,
            [],
        ),
        (
            {"aaa111": "charity", "bbb222": False, "ccc333": 10},
            TEST_SCHEMA_1,
            Eoi_Decision.FAIL,
            [],
        ),
        (
            {"aaa111": "charity", "bbb222": True, "ccc333": 15},
            TEST_SCHEMA_1,
            Eoi_Decision.PASS_WITH_CAVEATS,
            ["Try not to cut down trees: This is a bit high"],
        ),
        (
            {"eee555": "b", "ccc333": 15},
            TEST_SCHEMA_1,
            Eoi_Decision.PASS_WITH_CAVEATS,
            [
                "Try not to cut down trees: This is a bit high",
                "Caveat heading: some caveat text",
            ],
        ),
    ],
)
def test_schema_parsing(answers: dict, schema, exp_result, exp_caveats):
    # Create a copy of the test form and update with supplied answers for this scenario
    input_forms = deepcopy(TEST_EOI_FORMS_1)
    for answer in answers.items():
        for form in input_forms:
            for question in form["questions"]:
                for x in [field for field in question["fields"] if field["key"] == answer[0]]:
                    x["answer"] = answer[1]

    # get a result
    result = evaluate_eoi_response(schema, input_forms)

    # confirm result is as expected
    assert result["decision"] == exp_result
    assert result["caveats"] == exp_caveats

