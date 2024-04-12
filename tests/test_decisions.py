from copy import deepcopy

import pytest
from fsd_utils import Decision
from fsd_utils import evaluate_response
from fsd_utils.decision.evaluate_response_against_schema import (
    _evaluate_with_supplied_operators,
)


TEST_SCHEMA_1 = {
    "aaa111": [
        {"answerValue": "charity", "result": Decision.PASS, "caveat": None},
        {
            "answerValue": "parish_council",
            "result": Decision.PASS,
            "caveat": None,
        },
        {
            "answerValue": "plc",
            "result": Decision.FAIL,
            "caveat": None,
        },
    ],
    "bbb222": [
        {"answerValue": True, "result": Decision.PASS, "caveat": None},
        {"answerValue": False, "result": Decision.FAIL, "caveat": None},
    ],
    "ccc333": [
        {"answerValue": "10", "result": Decision.PASS, "caveat": None},
        {
            "answerValue": "15",
            "result": Decision.PASS_WITH_CAVEATS,
            "caveat": "Try not to cut down trees: This is a bit high",
        },
        {"answerValue": "20", "result": Decision.FAIL, "caveat": None},
    ],
    "eee555": [
        {"answerValue": "a", "result": Decision.PASS, "caveat": None},
        {
            "answerValue": "b",
            "result": Decision.PASS_WITH_CAVEATS,
            "caveat": "Caveat heading: some caveat text",
        },
        {"answerValue": "c", "result": Decision.FAIL, "caveat": None},
    ],
    "fff666": [
        {
            "operator": "<=",
            "compareValue": 4,
            "result": Decision.PASS,
            "caveat": None,
        },
        {
            "operator": ">=",
            "compareValue": 5,
            "result": Decision.PASS_WITH_CAVEATS,
            "caveat": "A caveat: Try and reduce this",
        },
        {
            "operator": ">=",
            "compareValue": 10,
            "result": Decision.FAIL,
            "caveat": None,
        },
    ],
    # add a deliberatly weird set of conditions
    "ggg777": [
        {"answerValue": "10", "result": Decision.PASS, "caveat": None},
        {"answerValue": "7", "result": Decision.PASS, "caveat": None},
        {
            "operator": "<",
            "compareValue": 10,
            "result": Decision.PASS_WITH_CAVEATS,
            "caveat": "A caveat",
        },
        {
            "operator": ">",
            "compareValue": 10,
            "result": Decision.FAIL,
            "caveat": None,
        },
    ],
}


# Test forms that will pass all the conditions in TEST_SCHEMA_1
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
                        "answer": "10",
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
                        "answer": "3",
                        "key": "fff666",
                        "title": "Pass or fail based on number",
                        "type": "NumberField",
                    },
                    {
                        "answer": "10",
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
        (  # All pass (no changes)
            {},
            TEST_SCHEMA_1,
            Decision.PASS,
            [],
        ),
        (  # All pass but one fail
            {"bbb222": False},
            TEST_SCHEMA_1,
            Decision.FAIL,
            [],
        ),
        (  # One pass with caveats, one fail
            {"ccc333": "15", "bbb222": False},
            TEST_SCHEMA_1,
            Decision.FAIL,
            [],
        ),
        (  # All pass but one pass with caveats
            {"ccc333": "15"},
            TEST_SCHEMA_1,
            Decision.PASS_WITH_CAVEATS,
            ["Try not to cut down trees: This is a bit high"],
        ),
        (  # Most pass but 2 pass with caveats - one number, one string, both value based
            {"eee555": "b", "ccc333": "15"},
            TEST_SCHEMA_1,
            Decision.PASS_WITH_CAVEATS,
            [
                "Try not to cut down trees: This is a bit high",
                "Caveat heading: some caveat text",
            ],
        ),
        (  # Most pass but 2 pass with caveats - one number - operator based, one string
            {"fff666": "6", "eee555": "b"},
            TEST_SCHEMA_1,
            Decision.PASS_WITH_CAVEATS,
            [
                "Caveat heading: some caveat text",
                "A caveat: Try and reduce this",
            ],
        ),
        (  # Most pass, one pass with caveats based on operator with contradicting value condition
            {"ggg777": "7"},
            TEST_SCHEMA_1,
            Decision.PASS_WITH_CAVEATS,
            [
                "A caveat",
            ],
        ),
        (  # Most pass, one pass with caveats based on operator
            {"ggg777": "3"},
            TEST_SCHEMA_1,
            Decision.PASS_WITH_CAVEATS,
            [
                "A caveat",
            ],
        ),
        (
            # most pass, one fails based on operator
            {"ggg777": "12"},
            TEST_SCHEMA_1,
            Decision.FAIL,
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
    result = evaluate_response(schema, input_forms)

    # confirm result is as expected
    assert result["decision"] == exp_result
    assert result["caveats"] == exp_caveats


TEST_OPERATOR_CONDITIONS = [
    {
        "operator": "<=",
        "compareValue": 4,
        "result": Decision.PASS,
        "caveat": None,
    },
    {
        "operator": ">=",
        "compareValue": 5,
        "result": Decision.PASS_WITH_CAVEATS,
        "caveat": "A caveat: more than 5",
    },
    {
        "operator": "==",
        "compareValue": 7,
        "result": Decision.PASS_WITH_CAVEATS,
        "caveat": "A caveat: equals 7",
    },
    {
        "operator": ">",
        "compareValue": 10,
        "result": Decision.FAIL,
        "caveat": None,
    },
    {
        "operator": "<",
        "compareValue": 0,
        "result": Decision.PASS,
        "caveat": None,
    },
]


@pytest.mark.parametrize(
    "answer,exp_decision,exp_caveats",
    [
        (2, Decision.PASS, []),
        ("2", Decision.PASS, []),
        (-1, Decision.PASS, []),
        ("-1", Decision.PASS, []),
        (5, Decision.PASS_WITH_CAVEATS, ["A caveat: more than 5"]),
        ("5", Decision.PASS_WITH_CAVEATS, ["A caveat: more than 5"]),
        (
            7,
            Decision.PASS_WITH_CAVEATS,
            ["A caveat: more than 5", "A caveat: equals 7"],
        ),
        (
            "7",
            Decision.PASS_WITH_CAVEATS,
            ["A caveat: more than 5", "A caveat: equals 7"],
        ),
        (12, Decision.FAIL, []),
        ("12", Decision.FAIL, []),
    ],
)
def test_evaluate_operators(answer, exp_decision, exp_caveats):
    result = _evaluate_with_supplied_operators(TEST_OPERATOR_CONDITIONS, answer)
    assert result[0] == exp_decision
    assert result[1] == exp_caveats


@pytest.mark.parametrize(
    "operator",
    [
        ("<"),
        (">"),
        ("<="),
        (">="),
        ("=="),
    ],
)
def test_operator_validation_success(operator):
    condition = {
        "operator": operator,
        "compareValue": 4,
        "result": Decision.PASS,
        "caveat": None,
    }
    _evaluate_with_supplied_operators([condition], 1)
    # Should be no exception - will fail if one is thrown


@pytest.mark.parametrize(
    "operator",
    [
        ("<X"),
        (""),
        ("randomsomethingelse"),
        ("*"),
        ("and"),
        (None),
    ],
)
def test_operator_validation_failures(operator):
    condition = {
        "operator": operator,
        "compareValue": 4,
        "result": Decision.PASS,
        "caveat": None,
    }

    with pytest.raises(ValueError):
        _evaluate_with_supplied_operators([condition], 1)


def test_no_questions_hit_conditions():
    TEST_SCHEMA = {
        "does_not_exist": [
            {"answerValue": True, "result": Decision.PASS, "caveat": None},
            {"answerValue": False, "result": Decision.FAIL, "caveat": None},
        ],
    }
    result = evaluate_response(TEST_SCHEMA, TEST_EOI_FORMS_1)
    assert result["decision"] == Decision.PASS
    assert result["caveats"] == []


@pytest.mark.parametrize(
    "supplied_answer",
    [
        "a1",
        "--2",
        "-a3.356345",
        "400099.asdf",
        "£234",
        "£234234.00",
        "hello there",
        "45,6",
        "123£$%^&*()''`\"",
    ],
)
def test_answer_validation_failure(supplied_answer):
    condition = {
        "operator": "<",
        "compareValue": 4,
        "result": Decision.PASS,
        "caveat": None,
    }
    with pytest.raises(ValueError):
        _evaluate_with_supplied_operators([condition], supplied_answer)


@pytest.mark.parametrize(
    "supplied_answer",
    ["1", 1, "-2", "-3.356345", "400099.234234", 3434.5656, 0, "00000", 0000],
)
def test_answer_validation_success(supplied_answer):
    condition = {
        "operator": "<",
        "compareValue": 4,
        "result": Decision.PASS,
        "caveat": None,
    }
    _evaluate_with_supplied_operators([condition], supplied_answer)
