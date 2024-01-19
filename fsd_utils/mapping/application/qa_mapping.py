from collections import defaultdict

from flask import current_app
from fsd_utils import NotifyConstants
from fsd_utils.mapping.application.application_utils import format_checkbox
from fsd_utils.mapping.application.application_utils import format_date_month_year
from fsd_utils.mapping.application.application_utils import format_month_year
from fsd_utils.mapping.application.application_utils import format_radio_field
from fsd_utils.mapping.application.free_text import FreeText
from fsd_utils.mapping.application.multi_input import MultiInput

from answer_displayers.CheckboxesField import CheckboxesFieldDisplayer
from answer_displayers.ClientSideFileUploadField import ClientSideFileUploadFieldDisplayer
from answer_displayers.RadiosField import RadiosFieldDisplayer
from answer_displayers.TextField import TextFieldDisplayer
from answer_displayers.YesNoField import YesNoFieldDisplayer
from answer_displayers.MultiInputField import MultiInputFieldDisplayer
from answer_displayers.DatePartsField import DatePartsFieldDisplayer
from answer_displayers.MonthYearField import MonthYearFieldDisplayer
from answer_displayers.FreeTextField import FreeTextFieldDisplayer

def extract_questions_and_answers(forms):
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
                            questions_answers[form_name][
                                field["title"]
                            ]=ClientSideFileUploadFieldDisplayer(answer).as_txt

                        elif isinstance(answer, bool) and field["type"] == "list":
                            questions_answers[form_name][
                                field["title"]
                            ]=YesNoFieldDisplayer(answer).as_txt

                        elif isinstance(answer, list) and field["type"] == "multiInput":
                            questions_answers[form_name][
                                field["title"]
                            ]=MultiInputFieldDisplayer(answer).as_txt

                        elif field["type"] == "freeText":
                            questions_answers[form_name][
                                field["title"]
                            ]=FreeTextFieldDisplayer(answer).as_txt

                        elif isinstance(answer, list) and field["type"] == "list":
                            questions_answers[form_name][
                                field["title"]
                            ]=CheckboxesFieldDisplayer(answer).as_txt

                        elif isinstance(answer, str) and field["type"] == "list":
                            questions_answers[form_name][
                                field["title"]
                            ]=RadiosFieldDisplayer(answer).as_txt

                        elif field["type"] == "monthYear":
                            questions_answers[form_name][
                                field["title"]
                            ]=MonthYearFieldDisplayer(answer).as_txt

                        elif field["type"] == "date":
                            questions_answers[form_name][
                                field["title"]
                            ]=DatePartsFieldDisplayer(answer).as_txt

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
                                # We only end up here if dont have a class to support this type?
                                questions_answers[form_name][field["title"]] = TextFieldDisplayer(answer).as_txt
    except Exception as e:
        current_app.logger.error(f"Error occurred while processing form data: {e}")
        current_app.logger.error(f"Could not map the data for form: {form_name}")
        raise Exception(f"Could not map the data for form: {form_name}")
    return questions_answers
