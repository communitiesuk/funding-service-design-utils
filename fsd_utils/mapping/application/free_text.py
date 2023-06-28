from bs4 import BeautifulSoup
from flask import current_app


class FreeText:
    indent = " " * 5

    @classmethod
    def remove_html_tags(cls, answer):
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

            if not soup.find():
                return answer.strip()

            if soup.ol:
                ol_tags = soup.find_all("ol")
                for ol in ol_tags:
                    li_tags = ol.find_all("li")
                    for index, li in enumerate(li_tags, start=1):
                        if li.get_text() == "\xa0":
                            continue
                        li.replace_with(f"{cls.indent}{str(index)}. {li.get_text()}\n")

            if soup.ul:
                ul_tags = soup.find_all("ul")
                for ul in ul_tags:
                    li_tags = ul.find_all("li")
                    for index, li in enumerate(li_tags, start=1):
                        if li.get_text() == "\xa0":
                            continue
                        li.replace_with(f"{cls.indent}. {li.get_text()}\n")

            plain_text = soup.get_text().strip()
            return plain_text

        except Exception as e:
            current_app.logger.error(
                f"Error occurred while processing HTML tag: {answer}", e
            )
            return answer
