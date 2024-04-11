from enum import IntEnum


class Decision(IntEnum):
    PASS = 0
    PASS_WITH_CAVEATS = 1
    FAIL = 2


VALID_OPERATORS = ["<", "<=", "==", ">=", ">"]


def _evaluate_with_supplied_operators(
    conditions_to_evaluate: list, supplied_answer: any
) -> tuple[Decision, list]:
    """Evaluates an expression built from the operator in the schmea, the value to compare, and the supplied answer.
    Uses the result of the evaluation to return a decision and applicable caveats
    Casts the value to an integer for comparison

    Args:
        conditions_to_evaluate (list): List of conditions from schema
        supplied_answer (any): Answer supplied to this question

    Raises:
        ValueError: If the operator from the schema is not supported, or if the supplied answer
        cannot be converted to a float

    Returns:
        tuple[Decision, list]: Tuple of the decision and the caveats (if there are any)
    """
    decision = Decision.PASS
    caveats = []
    for ec in conditions_to_evaluate:
        # validate supplied operator
        if ec["operator"] not in VALID_OPERATORS:
            raise ValueError(f"Operator {ec['operator']} is not supported")

        # validate that answer is numeric
        try:
            answer_as_number = float(supplied_answer)
        except ValueError:
            raise ValueError(
                f"Answer {supplied_answer} is not numeric so cannot be used with this condition: "
                f"[{ec['operator']} {ec['compareValue']}]"
            )

        # construct evaluation expression
        expression = f"answer {ec['operator']} value"

        # evaluation using supplied operator
        if eval(expression, {"answer": answer_as_number, "value": ec["compareValue"]}):
            # We met this condition
            decision = max(decision, ec["result"])
            if ec["caveat"]:
                caveats.append(ec["caveat"])

    if decision == Decision.FAIL:
        return decision, []  # don't return caveats for failure
    else:
        return decision, caveats


def evaluate_response(schema: dict, forms: dict) -> dict:
    """Takes in a decision schema and a set of forms containing responses, then makes a decision on the outcome

    Args:
        schema (dict): Schema defining decisions based on answers
        forms (dict): Response forms in form-builder json format

    Returns:
        dict: Results of decision:
            decision: value of Decision ENUM
            caveats: list of strings of caveats for answers if decision is 'Pass with caveats', otherwise empty list

    """
    result = {"decision": Decision.PASS, "caveats": []}

    # Loop through every form, then every response in that form
    for form in forms:
        for question in form["questions"]:
            for response in question["fields"]:
                questionId = response["key"]

                # Find out if there are any conditions that apply to this question
                if conditions := schema.get(questionId, None):

                    # Find out if there are any value-based conditions that match the response given for this question
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

                    # Gather any operator-based conditions that apply to this question
                    if eval_conditions := [c for c in conditions if "operator" in c]:

                        # Got and get a decision based on this operator condition
                        decision, caveats = _evaluate_with_supplied_operators(
                            eval_conditions, response["answer"]
                        )

                        # Update result object with result of evaluating the operator-condition
                        result["decision"] = max(result["decision"], decision)
                        result["caveats"] += caveats

                    # If we failed on this question, we don't need to evaluate any further, just return a fail
                    if result["decision"] == Decision.FAIL:
                        return {"decision": Decision.FAIL, "caveats": []}

    return result
