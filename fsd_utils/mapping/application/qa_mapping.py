from collections import defaultdict

from flask import current_app
from fsd_utils import NotifyConstants
from fsd_utils.mapping.application.application_utils import format_checkbox
from fsd_utils.mapping.application.application_utils import format_date_month_year
from fsd_utils.mapping.application.application_utils import format_month_year
from fsd_utils.mapping.application.application_utils import format_radio_field
from fsd_utils.mapping.application.application_utils import NO
from fsd_utils.mapping.application.application_utils import YES
from fsd_utils.mapping.application.free_text import FreeText
from fsd_utils.mapping.application.languages import EN
from fsd_utils.mapping.application.languages import SUPPORTED_LANGUAGES
from fsd_utils.mapping.application.multi_input import MultiInput


def extract_questions_and_answers(forms, language=EN) -> dict:
    if not language and language not in SUPPORTED_LANGUAGES:
        language = EN

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
                                YES[language] if answer else NO[language]
                            )

                        elif isinstance(answer, list) and field["type"] == "multiInput":
                            questions_answers[form_name][
                                field["title"]
                            ] = MultiInput.map_multi_input_data(answer, language)

                        elif field["type"] == "freeText":
                            clean_html_answer = FreeText.remove_html_tags(answer)

                            questions_answers[form_name][
                                field["title"]
                            ] = clean_html_answer

                        elif isinstance(answer, list) and field["type"] == "list":
                            questions_answers[form_name][
                                field["title"]
                            ] = format_checkbox(answer)

                        elif isinstance(answer, str) and field["type"] == "list":
                            questions_answers[form_name][
                                field["title"]
                            ] = format_radio_field(answer)

                        elif field["type"] == "monthYear":
                            questions_answers[form_name][
                                field["title"]
                            ] = format_month_year(answer)

                        elif field["type"] == "date":
                            questions_answers[form_name][
                                field["title"]
                            ] = format_date_month_year(answer)

                        else:
                            # we dont want to display boolean question
                            # (Do you want to mark this section as complete?)
                            if (
                                field.get("type") == "boolean"
                                and field.get("title").strip().lower()
                                == "do you want to mark this section as complete?"
                            ):
                                continue
                            else:
                                questions_answers[form_name][field["title"]] = answer
    except Exception as e:
        current_app.logger.error(f"Error occurred while processing form data: {e}")
        current_app.logger.error(f"Could not map the data for form: {form_name}")
        raise Exception(f"Could not map the data for form: {form_name}")
    return questions_answers
