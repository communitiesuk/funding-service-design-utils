from enum import Enum
import pytest
from copy import deepcopy
from fsd_utils import evaluate_eoi_response, Eoi_Decision
from unittest.mock import MagicMock
from fsd_utils.eoi.evaluate_eoi_response import _evaluate_with_supplied_operators


TEST_SCHEMA_1 = {
    "aaa111": [
        {"answerValue": "charity", "result": Eoi_Decision.PASS, "caveat": None},
        {
            "answerValue": "parish_council",
            "result": Eoi_Decision.PASS,
            "caveat": None,
        },
        {
            "answerValue": "plc",
            "result": Eoi_Decision.FAIL,
            "caveat": None,
        },
    ],
    "bbb222": [
        {"answerValue": True, "result": Eoi_Decision.PASS, "caveat": None},
        {"answerValue": False, "result": Eoi_Decision.FAIL, "caveat": None},
    ],
    "ccc333": [
        {"answerValue": 10, "result": Eoi_Decision.PASS, "caveat": None},
        {
            "answerValue": 15,
            "result": Eoi_Decision.PASS_WITH_CAVEATS,
            "caveat": "Try not to cut down trees: This is a bit high",
        },
        {"answerValue": 20, "result": Eoi_Decision.FAIL, "caveat": None},
    ],
    "eee555": [
        {"answerValue": "a", "result": Eoi_Decision.PASS, "caveat": None},
        {
            "answerValue": "b",
            "result": Eoi_Decision.PASS_WITH_CAVEATS,
            "caveat": "Caveat heading: some caveat text",
        },
        {"answerValue": "c", "result": Eoi_Decision.FAIL, "caveat": None},
    ],
    "fff666": [
        {
            "operator": "<=",
            "compareValue": 4,
            "result": Eoi_Decision.PASS,
            "caveat": None,
        },
        {
            "operator": ">=",
            "compareValue": 5,
            "result": Eoi_Decision.PASS_WITH_CAVEATS,
            "caveat": "A caveat: Try and reduce this",
        },
        {
            "operator": ">=",
            "compareValue": 10,
            "result": Eoi_Decision.FAIL,
            "caveat": None,
        },
    ],
    # add a deliberatly weird set of conditions
    "ggg777": [
        {"answerValue": 10, "result": Eoi_Decision.PASS, "caveat": None},
        {"answerValue": 7, "result": Eoi_Decision.PASS, "caveat": None},
        {
            "operator": "<",
            "compareValue": 10,
            "result": Eoi_Decision.PASS_WITH_CAVEATS,
            "caveat": "A caveat",
        },
        {
            "operator": ">",
            "compareValue": 10,
            "result": Eoi_Decision.FAIL,
            "caveat": None,
        },
    ]
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
                        "answer": 3,
                        "key": "fff666",
                        "title": "Pass or fail based on number",
                        "type": "NumberField",
                    },
                    {
                        "answer": 10,
                        "key": "ggg777",
                        "title": "Pass or fail based on number",
                        "type": "NumberField",
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
        (
            {"fff666": 6, "eee555": "b"},
            TEST_SCHEMA_1,
            Eoi_Decision.PASS_WITH_CAVEATS,
            [
                "Caveat heading: some caveat text",
                "A caveat: Try and reduce this",
            ],
        ),
        (
            {"ggg777": 7},
            TEST_SCHEMA_1,
            Eoi_Decision.PASS_WITH_CAVEATS,
            [
                "A caveat",
            ],
        ),
        (
            {"ggg777": 3},
            TEST_SCHEMA_1,
            Eoi_Decision.PASS_WITH_CAVEATS,
            [
                "A caveat",
            ],
        ),
        (
            {"ggg777": 12},
            TEST_SCHEMA_1,
            Eoi_Decision.FAIL,
            [],
        ),
    ],
)
def test_schema_parsing(answers: dict, schema, exp_result, exp_caveats):
    # Create a copy of the test form and update with supplied answers for this scenario
    input_forms = deepcopy(TEST_EOI_FORMS_1)
    for answer in answers.items():
        for form in input_forms:
            for question in form["questions"]:
                for x in [
                    field for field in question["fields"] if field["key"] == answer[0]
                ]:
                    x["answer"] = answer[1]

    # get a result
    result = evaluate_eoi_response(schema, input_forms)

    # confirm result is as expected
    assert result["decision"] == exp_result
    assert result["caveats"] == exp_caveats


TEST_OPERATOR_CONDITIONS = [
    {
        "operator": "<=",
        "compareValue": 4,
        "result": Eoi_Decision.PASS,
        "caveat": None,
    },
    {
        "operator": ">=",
        "compareValue": 5,
        "result": Eoi_Decision.PASS_WITH_CAVEATS,
        "caveat": "A caveat: more than 5",
    },
    {
        "operator": "==",
        "compareValue": 7,
        "result": Eoi_Decision.PASS_WITH_CAVEATS,
        "caveat": "A caveat: equals 7",
    },
    {
        "operator": ">",
        "compareValue": 10,
        "result": Eoi_Decision.FAIL,
        "caveat": None,
    },
    {
        "operator": "<",
        "compareValue": 0,
        "result": Eoi_Decision.PASS,
        "caveat": None,
    },
]


@pytest.mark.parametrize(
    "answer,exp_decision,exp_caveats",
    [
        (2, Eoi_Decision.PASS, []),
        (-1, Eoi_Decision.PASS, []),
        (5, Eoi_Decision.PASS_WITH_CAVEATS, ["A caveat: more than 5"]),
        (
            7,
            Eoi_Decision.PASS_WITH_CAVEATS,
            ["A caveat: more than 5", "A caveat: equals 7"],
        ),
        (12, Eoi_Decision.FAIL, []),
    ],
)
def test_evaluate_operators(answer, exp_decision, exp_caveats):
    result = _evaluate_with_supplied_operators(TEST_OPERATOR_CONDITIONS, answer)
    assert result[0] == exp_decision
    assert result[1] == exp_caveats


@pytest.mark.parametrize(
    "operator,exp_exception",
    [
        ("<", False),
        (">", False),
        ("<=", False),
        (">=", False),
        ("==", False),
        ("<X", True),
        ("", True),
        ("randomsomethingelse", True),
        ("*", True),
        ("and", True),
        (None, True),
    ],
)
def test_operator_validation(operator, exp_exception):
    condition = {
        "operator": operator,
        "compareValue": 4,
        "result": Eoi_Decision.PASS,
        "caveat": None,
    }
    if exp_exception:
        with pytest.raises(ValueError):
            result = _evaluate_with_supplied_operators([condition], 1)
    else:
        _evaluate_with_supplied_operators([condition], 1)
