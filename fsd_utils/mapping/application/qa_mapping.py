from collections import defaultdict

from bs4 import BeautifulSoup
from flask import current_app
from fsd_utils import NotifyConstants
from fsd_utils.mapping.application.application_utils import format_checkbox
from fsd_utils.mapping.application.multi_input import MultiInput


def remove_html_tags(answer):
    """
    Removes HTML tags from the provided answer and returns the cleaned text.

    Args:
        answer (str): The answer containing HTML tags.

    Returns:
        str: The cleaned text with HTML tags removed.
    """

    try:
        if answer is None or isinstance(answer, (bool, list)):
            return answer

        # Check if answer looks like a URL
        if answer.startswith("http://") or answer.startswith("https://"):
            return answer

        soup = BeautifulSoup(answer, "html.parser")
        indent = " " * 5

        if not soup.find():
            return answer.strip()

        if soup.ol:
            ol_tags = soup.find_all("ol")
            for ol in ol_tags:
                li_tags = ol.find_all("li")
                for index, li in enumerate(li_tags, start=1):
                    if li.get_text() == "\xa0":
                        continue
                    li.replace_with(f"{indent}{str(index)}. {li.get_text()}\n")

        if soup.ul:
            ul_tags = soup.find_all("ul")
            for ul in ul_tags:
                li_tags = ul.find_all("li")
                for index, li in enumerate(li_tags, start=1):
                    if li.get_text() == "\xa0":
                        continue
                    li.replace_with(f"{indent}. {li.get_text()}\n")

        plain_text = soup.get_text().strip()
        return plain_text

    except Exception as e:
        current_app.logger.error(
            f"Error occurred while processing HTML tag: {answer}", e
        )
        return answer


def extract_questions_and_answers_from_json_blob(forms) -> dict:
    """function takes the form data and returns
    dict of questions & answers.
    """
    questions_answers = defaultdict(dict)
    try:
        for count, form in enumerate(forms, start=1):
            form_name = form["name"]
            current_app.logger.info(f"Form {count}) {form_name}")
            if form_name in form[NotifyConstants.APPLICATION_NAME_FIELD]:
                for question in form[NotifyConstants.APPLICATION_QUESTIONS_FIELD]:
                    for field in question["fields"]:
                        answer = field.get("answer")

                        if field["type"] == "file":
                            # we check if the question type is "file"
                            # then we remove the aws
                            # key attached to the answer
                            if isinstance(answer, str):
                                questions_answers[form_name][
                                    field["title"]
                                ] = answer.split("/")[-1]
                            else:
                                questions_answers[form_name][field["title"]] = answer

                        elif isinstance(answer, bool) and field["type"] == "list":

                            questions_answers[form_name][field["title"]] = (
                                "Yes" if answer else "No"
                            )

                        elif isinstance(answer, list) and field["type"] == "multiInput":
                            questions_answers[form_name][
                                field["title"]
                            ] = MultiInput.map_multi_input_data(answer)

                        elif field["type"] == "freeText":
                            clean_html_answer = remove_html_tags(answer)

                            questions_answers[form_name][
                                field["title"]
                            ] = clean_html_answer

                        elif isinstance(answer, list) and field["type"] == "list":
                            questions_answers[form_name][
                                field["title"]
                            ] = format_checkbox(answer)

                        else:
                            questions_answers[form_name][field["title"]] = answer
    except Exception as e:
        current_app.logger.error(f"Error occurred while processing form data: {e}")
        current_app.logger.error(f"Could not map the data for form: {form_name}")
        raise Exception(f"Could not map the data for form: {form_name}")
    return questions_answers
