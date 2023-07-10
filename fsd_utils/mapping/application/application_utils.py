import calendar
import re
from io import StringIO

from flask import current_app


def convert_bool_value(data):
    try:

        def convert_values(value):
            if value is None:
                return "Not provided"
            elif value is True:
                return "Yes"
            elif value is False:
                return "No"
            else:
                return value

        if isinstance(data, list):
            if all(isinstance(sublist, list) for sublist in data):
                converted_data = [
                    [convert_values(value) for value in sublist] for sublist in data
                ]
            else:
                converted_data = [convert_values(value) for value in data]
        else:
            converted_data = convert_values(data)

        return converted_data
    except Exception as e:
        current_app.logger.error(f"Could not convert boolean values, {e}")


def format_answer(answer):
    try:
        if answer is None:
            return "Not provided"

        if "null" in answer:
            return re.sub(r"\s*null\s*,?", "", answer)

        if isinstance(answer, str):
            if answer.startswith("http") or answer.startswith("https"):
                return answer
            elif "-" in answer:
                return answer.replace("-", " ")

        if isinstance(answer, list):
            return [
                a.replace("'", "").replace("-", " ")
                if isinstance(a, str) and "-" in a
                else a
                for a in answer
            ]
        else:

            return answer
    except Exception as e:
        current_app.logger.error(f"Could not format the answer: {e}")


def simplify_title(section_name, remove_text: list):
    try:
        section = section_name.split("-")
        simplified_title = []

        for i, text in enumerate(section):
            if text in remove_text:
                simplified_title = section[:i]
                break

        if not simplified_title:
            simplified_title = section

        return simplified_title
    except Exception as e:
        current_app.logger.error(f"Could not simplify the section title, {e}")


def format_checkbox(answer):
    formatted_elements = []
    indent = " " * 5
    for index, element in enumerate(answer, start=1):
        separator = f"{indent}." if index > 1 else "."
        if "-" in element:
            sub_elements = element.split("-")
            formatted_sub_elements = " ".join(sub_elements).strip()
            formatted_elements.append(f"{separator} {formatted_sub_elements}")
        else:
            formatted_elements.append(f"{separator} {element}")

    return "\n".join(formatted_elements)


def generate_text_of_application(q_and_a: dict, fund_name: str):
    output = StringIO()

    output.write(f"********* {fund_name} **********\n")

    for section_name, values in q_and_a.items():
        title = simplify_title(section_name, remove_text=["cof", "ns"])
        output.write(f"\n* {' '.join(title).capitalize()}\n\n")
        for questions, answers in values.items():
            output.write(f"  Q) {questions}\n")
            output.write(f"  A) {format_answer(answers)}\n\n")
    return output.getvalue()


def number_to_month(number, iso_key):
    """Converts a month number to its corresponding month name."""
    try:
        if iso_key == "month":
            month_name = calendar.month_name[number]
            return month_name
        else:
            return number
    except IndexError:
        current_app.logger.warn("Invalid month number")
        return number
