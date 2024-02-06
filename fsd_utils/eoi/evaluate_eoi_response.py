from enum import IntEnum


class Eoi_Decision(IntEnum):
    PASS = 0
    PASS_WITH_CAVEATS = 1
    FAIL = 2


VALID_OPERATORS = ["<", "<=", "==", ">=", ">"]


def _evaluate_with_supplied_operators(
    conditions_to_evaluate: list, supplied_answer: any
) -> tuple[Eoi_Decision, list]:
    """Evaluates an expression built from the operator in the schmea, the value to compare, and the supplied answer. Uses the result of the evaluation to return a decision and applicable caveats

    Args:
        conditions_to_evaluate (list): List of conditions from schema
        supplied_answer (any): Answer supplied to this question

    Raises:
        ValueError: If the operator from the schema is not supported

    Returns:
        tuple[Eoi_Decision, list]: Tuple of the decision and the caveats (if there are any)
    """
    decision = Eoi_Decision.PASS
    caveats = []
    for ec in conditions_to_evaluate:
        # validate supplied operator
        if ec["operator"] not in VALID_OPERATORS:
            raise ValueError(f"Operator {ec['operator']} is not supported")

        # construct evaluation expression
        expression = f"answer {ec['operator']} value"

        # evaluation using supplied operator
        if eval(expression, {"answer": supplied_answer, "value": ec["compareValue"]}):
            # We met this condition
            decision = max(decision, ec["result"])
            if ec["caveat"]:
                caveats.append(ec["caveat"])

    if decision == Eoi_Decision.FAIL:
        return decision, []  # don't return caveats for failure
    else:
        return decision, caveats


def evaluate_eoi_response(schema: dict, forms: dict) -> dict:
    """Takes in an EOI schema and a set of forms containing responses, then makes a decision on the EOI outcome

    Args:
        schema (dict): Schema defining decisions based on answers
        forms (dict): Response forms in form-builder json format

    Returns:
        dict: Results of decision:
            decision: value of Eoi_Decision ENUM
            caveats: list of strings of caveats for answers if decision is 'Pass with caveats', otherwise empty list

    """
    result = {"decision": Eoi_Decision.PASS, "caveats": []}

    for form in forms:
        for question in form["questions"]:
            for response in question["fields"]:
                questionId = response["key"]
                if conditions := schema.get(questionId, None):
                    if applicable_condition := next(
                        (
                            c
                            for c in conditions
                            if c.get("answerValue", None) == response["answer"]
                        ),
                        None,
                    ):
                        result["decision"] = max(
                            result["decision"], applicable_condition["result"]
                        )
                        if applicable_condition["caveat"]:
                            result["caveats"].append(applicable_condition["caveat"])
                    if eval_conditions := [c for c in conditions if "operator" in c]:
                        decision, caveats = _evaluate_with_supplied_operators(
                            eval_conditions, response["answer"]
                        )
                        result["decision"] = max(result["decision"], decision)
                        result["caveats"] += caveats

    return result