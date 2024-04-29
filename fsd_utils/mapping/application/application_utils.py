import calendar
import re
from io import StringIO

from flask import current_app
from fsd_utils.mapping.application.languages import EN
from fsd_utils.mapping.application.languages import NO
from fsd_utils.mapping.application.languages import NOT_PROVIDED
from fsd_utils.mapping.application.languages import SUPPORTED_LANGUAGES
from fsd_utils.mapping.application.languages import YES


def convert_bool_value(data, language=EN):
    if not language and language not in SUPPORTED_LANGUAGES:
        language = EN

    try:

        def convert_values(value):
            if value is None or value == "None":
                return NOT_PROVIDED[language]
            if isinstance(value, bool):
                return YES[language] if value else NO[language]
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


def format_answer(answer, language):
    try:
        if answer is None or answer == "None":
            return NOT_PROVIDED[language]

        if "null" in answer:
            return re.sub(r"\s*null\s*,?", "", answer)

        if isinstance(answer, list):
            return [a.replace("'", "") for a in answer if isinstance(a, str)]

        return answer
    except Exception:
        current_app.logger.info(f"No formatting required for an answer: {answer}")


def simplify_title(section_name: str, remove_text: list) -> list:
    """
    Simplify a section title by removing specified text elements.

    This function takes a section title as input and removes specific text elements
    based on the provided 'remove_text' list. It splits the section title by hyphens
    and removes elements from the beginning until it encounters the first match in
    'remove_text'. If no match is found, the original section title is returned.

    Parameters:
    - section_name (str): The original section title to be simplified.
    - remove_text (list): A list of text elements to be removed from the title.

    Returns:
    - simplified_title (list): A list containing the simplified section title
      after removing the specified elements.
    """
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
        current_app.logger.warning(f"Could not simplify the section title, {e}")


def format_checkbox(answer: list) -> str:
    """
    Format a list of elements into a checkbox-style list.

    This function takes a list of elements as input and formats them into a
    checkbox-style list with proper indentation and capitalization. It processes
    each element, splitting hyphenated elements if present, and returns the formatted
    checkbox-style list as a string.

    Parameters:
    - answer (list): The list of elements to be formatted.

    Returns:
    - formatted_list (str): The formatted checkbox-style list as a string.
    """
    formatted_elements = []
    indent = " " * 5
    for index, element in enumerate(answer, start=1):
        separator = f"{indent}." if index > 1 else "."
        if "-" in element:
            sub_elements = element.split("-")
            formatted_sub_elements = " ".join(sub_elements).strip().capitalize()
            formatted_elements.append(f"{separator} {formatted_sub_elements}")
        else:
            formatted_elements.append(f"{separator} {element.capitalize()}")

    return "\n".join(formatted_elements)


def format_radio_field(answer: str) -> str:
    """
    Format a radio field answer for better readability.

    This function takes an answer from a radio field and applies formatting to
    enhance its readability. It handles cases where the answer is a URL, a boolean,
    a list, or a string with hyphens. It capitalizes the first letter of each word
    and joins them with spaces.

    Parameters:
    - answer: The radio field answer to be formatted.

    Returns:
    - formatted_answer: The formatted answer for improved readability.
    """
    try:
        if answer is None or isinstance(answer, (bool, list)):
            return answer

        # Check if answer looks like a URL
        if answer.startswith("http://") or answer.startswith("https://"):
            return answer

        if "-" in answer:
            answer = answer.split("-")
            formatted_answer = " ".join(answer).strip().capitalize()
            return formatted_answer
        else:
            return answer.capitalize()

    except Exception:  # noqa
        current_app.logger.info(
            "continue: the answer doesn't seem to be a radio field."
        )
        return answer


def generate_text_of_application(q_and_a: dict, fund_name: str, language=EN) -> str:
    """
    Generate a formatted text document for an application with questions and answers.

    This function takes a dictionary of questions and answers ('q_and_a') and the name
    of a fund ('fund_name'). It creates a formatted text document containing the fund
    name, section titles derived from 'q_and_a' keys, and corresponding questions and
    answers. Text is formatted with section titles, question and answer numbering, and
    specific text elements are simplified as specified. The resulting output is
    returned as a string.

    Parameters:
    - q_and_a (dict): A dictionary of questions and answers.
    - fund_name (str): The name of the fund.
    - language (str): "en" or "cy", the language to use.

    Returns:
    - application_text (str): A formatted text output for the application.
    """
    if not language and language not in SUPPORTED_LANGUAGES:
        language = EN

    output = StringIO()

    output.write(f"********* {fund_name} **********\n")

    for section_name, values in q_and_a.items():
        title = simplify_title(
            section_name, remove_text=["cof", "ns", "cyp", "dpi", "hsra"]
        )
        output.write(f"\n* {' '.join(title).capitalize()}\n\n")
        for questions, answers in values.items():
            output.write(f"  Q) {questions}\n")
            output.write(f"  A) {format_answer(answers, language)}\n\n")
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
            date = f"{'0' + date if len(date) == 1 else date}"
            year = answer_text[0] if len(answer_text[0]) == 4 else answer_text[2]
            return f"{date} {month_name} {year}"
    except Exception as e:
        current_app.logger.warning(
            f"Invalid date-month-year formatting for answer: {answer}. Error: {str(e)}"
        )
    return answer
