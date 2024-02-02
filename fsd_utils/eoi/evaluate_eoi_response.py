from enum import IntEnum

class Eoi_Decision(IntEnum):
    PASS = 0
    PASS_WITH_CAVEATS = 1
    FAIL = 2

def evaluate_eoi_response(schema: dict, forms: dict) -> dict:
    result = {
        "decision": Eoi_Decision.PASS,
        "caveats": []
    }
    # input_forms[1]["questions"][0]["fields"]

    for form in forms:
        for question in form["questions"]:
            for response in question["fields"]:
                questionId = response["key"]
                if conditions := schema.get(questionId, None):
                    applicable_condition = conditions[response["answer"]]
                    result["decision"] = max(result["decision"], applicable_condition["result"])
                    if applicable_condition["caveat"]:
                        result["caveats"].append(applicable_condition["caveat"])
    return result