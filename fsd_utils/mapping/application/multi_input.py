from flask import current_app
from fsd_utils.mapping.application.application_utils import convert_bool_value
from fsd_utils.mapping.application.multi_input_utils import ProcessTypes


class MultiInput(ProcessTypes):
    @classmethod
    def indent(cls, indent_space):
        return " " * indent_space

    @classmethod
    def format_values(cls, value, index):
        return f"{cls.indent(5)} \n. {value}" if index != 1 else f". {value}"

    @classmethod
    def format_value_pair(cls, key, value):
        return f"{key}: {value}"

    @classmethod
    def format_keys_and_values(cls, key: str, value: list, index: enumerate):
        sanitised_values = convert_bool_value(value)
        values = "\n".join(
            [
                f"{cls.indent(6) if i == 1 else cls.indent(7)}. {str(item).strip()}"
                for i, item in enumerate(sanitised_values, start=1)
            ]
        )

        return (
            f"\n{cls.indent(5)}{str(key.strip())} \n {values}"  # noqa
            if index != 1
            else (f"{str(key.strip())} \n {values}")  # noqa
        )

    @classmethod
    def process_data(cls, sorted_data: dict) -> list:

        output = []
        for index, (key, value) in enumerate(sorted_data.items(), start=1):

            if isinstance(key, int):
                key = str(key)
            try:
                uuid = ProcessTypes.is_valid_uuid(key)  # noqa
                if uuid:
                    output.append(cls.format_values(value, index))

                if isinstance(value, list):
                    output.append(cls.format_keys_and_values(key, value, index))
                if not uuid and not isinstance(value, list):
                    output.append(cls.format_value_pair(key, value))

            except Exception as e:
                current_app.logger.error(f"Error occurred while processing data: {e}")
                current_app.logger.error(
                    f"Couldn't format the muti input data for: {sorted_data}"
                )
        return output

    @classmethod
    def map_multi_input_data(cls, multi_input_data: list[dict]):

        try:
            sorted_data = {}
            for item in multi_input_data:
                if len(item) < 2:
                    if isinstance(item, str):
                        cls._str_single_item(item, sorted_data)
                    if isinstance(item, dict):
                        cls._dict_single_item(item, sorted_data)
                else:
                    if isinstance(item, dict):
                        cls._dict_items(item, sorted_data)

            output = cls.process_data(sorted_data)
            output = "\n".join(output)
            return output

        except Exception as e:
            current_app.logger.error(
                f"Error occurred while processing the multi input data: {e}"
            )
            current_app.logger.error(
                f"Couldn't map the multi input data for: {multi_input_data}"
            )
