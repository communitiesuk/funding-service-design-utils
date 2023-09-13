import calendar
import re
from io import StringIO

from flask import current_app


def convert_bool_value(data):
    try:

        def convert_values(value):
            if value is None or value == "None":
                return "Not provided"
            if isinstance(value, bool):
                return "Yes" if value else "No"
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
        if answer is None or answer == "None":
            return "Not provided"

        if "null" in answer:
            return re.sub(r"\s*null\s*,?", "", answer)

        if isinstance(answer, list):
            return [a.replace("'", "") for a in answer if isinstance(a, str)]

        return answer
    except Exception:
        current_app.logger.error(f"No formatting required for an answer: {answer}")


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


def format_radio_field(answer):
    try:
        if answer is None or isinstance(answer, (bool, list)):
            return answer

        # Check if answer looks like a URL
        if answer.startswith("http://") or answer.startswith("https://"):
            return answer

        if "-" in answer:
            answer = answer.split("-")
            formatted_answer = " ".join(answer).strip()
            return formatted_answer
        else:
            return answer

    except Exception:  # noqa
        current_app.logger.info(
            "continue: the answer doesn't seem to be a radio field."
        )
        return answer


def generate_text_of_application(q_and_a: dict, fund_name: str):
    output = StringIO()

    output.write(f"********* {fund_name} **********\n")

    for section_name, values in q_and_a.items():
        title = simplify_title(section_name, remove_text=["cof", "ns"])
        output.write(f"\n** {' '.join(title).capitalize()} **\n\n")
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
        current_app.logger.warning("Invalid month number")
        return number


def format_month_year(answer):
    try:
        answer_text = answer.split("-")
        month = answer_text[0] if len(answer_text[0]) <= 2 else answer_text[1]
        month_name = calendar.month_name[int(month)]
        if month_name:
            year = answer_text[1] if len(answer_text[1]) == 4 else answer_text[0]
            return f"{month_name} {year}"
    except Exception as e:
        current_app.logger.warning(
            f"Invalid month-year formatting for answer: {answer}. Error: {str(e)}"
        )

    return answer


def format_date_month_year(answer):
    try:
        answer_text = answer.split("-")
        month = answer_text[1]
        month_name = calendar.month_name[int(month)]
        if month_name:
            date = answer_text[2] if len(answer_text[2]) <= 2 else answer_text[0]
            date = f"{'0'+date if len(date)==1 else date}"
            year = answer_text[0] if len(answer_text[0]) == 4 else answer_text[2]
            return f"{date} {month_name} {year}"
    except Exception as e:
        current_app.logger.warning(
            f"Invalid date-month-year formatting for answer: {answer}. Error: {str(e)}"
        )
    return answer
