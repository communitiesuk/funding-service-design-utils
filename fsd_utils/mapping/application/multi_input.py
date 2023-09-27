import json
import uuid

from flask import current_app
from fsd_utils.mapping.application.application_utils import convert_bool_value
from fsd_utils.mapping.application.application_utils import number_to_month


class MultiInput:
    @classmethod
    def indent(cls, indent_space):
        return " " * indent_space

    @classmethod
    def format_values(cls, value, index):
        """
        Format the given value based on the specified conditions.
        Args:
            value: The value to be formatted.
            index: The index of the value in the processing sequence.
        Returns:
            str: The formatted string representation of the value.
        """
        current_app.logger.info(f"[format_values] formatting data: {value}")
        return f"{cls.indent(5)}. {value}" if index != 1 else f". {value}"

    @classmethod
    def format_keys_and_values(cls, key: str, value: list, index: enumerate):

        """
        Format the given key-value pair based on specified conditions.
        Args:
            key: The key of the key-value pair.
            value: The value associated with the key.
            index: The index of the key-value pair in the processing sequence.
        Returns:
            str: The formatted string representation of the key-value pair.
        """

        current_app.logger.info(
            f"[format_keys_and_values] formatting data:{key}, {value}"
        )

        sanitised_values = convert_bool_value(value)

        values = "\n".join(
            [
                f"{cls.indent(6) if i == 1 else cls.indent(7)}. {str(item).strip()}"
                for i, item in enumerate(sanitised_values, start=1)
            ]
        )

        return (
            f"\n{cls.indent(5)}* {str(key.strip())} \n {values}"  # noqa
            if index != 1
            else (f"* {str(key.strip())} \n {values}")  # noqa
        )

    @classmethod
    def format_nested_data(cls, value):
        """
        Formats nested data based on specific keys and data and returns the formatted result.
        Args:
            value: A nested data structure to be processed and formatted.

        Returns:
            str: The formatted result obtained from the nested data.
        """
        current_app.logger.info(f"[format_nested_data] processing data: {value}")

        formatted_nested_values = []

        def get_validated_key(key, iso_keys):
            for iso_key in iso_keys:
                if iso_key in key:
                    return iso_key
            return key

        def process_value(inner_items):
            formatted_values = []
            iso_keys = ["date", "month", "year"]

            for k, v in inner_items.items():
                key = k.split("__")
                validated_key = get_validated_key(key, iso_keys)

                if any(iso_key in validated_key for iso_key in iso_keys):
                    value = number_to_month(v, validated_key)
                    formatted_values.append(f"{value}")
                elif v not in (None, " ", ""):
                    formatted_values.append(f"{v}")
            return " ".join(formatted_values)

        try:
            try:
                for inner_items in value:
                    if isinstance(inner_items, dict):
                        v = process_value(inner_items)
                        formatted_nested_values.append(f"{v},")
                    else:
                        if inner_items not in (None, " ", ""):
                            formatted_nested_values.append(f"{inner_items}")

            # handles all other nested multiple values
            except:  # noqa
                formatted_nested_values.append(
                    ", ".join(
                        map(
                            lambda item: ", ".join(
                                [f"{k}: {v}" for k, v in item.items()]
                            ),
                            value,
                        )
                    )
                )
        except:  # noqa
            current_app.logger.error(
                f"Couldn't format the multi input nested data for: {value}"
            )

        return " ".join(formatted_nested_values)

    @classmethod
    def process_data(cls, data):
        """
        Process the data dictionary and generate a formatted output list.
        Args:
            data (dict): The dictionary to be processed.
        Returns:
            list: The formatted output list generated from the data.
        """

        current_app.logger.info(f"[process_data] processing data: {data}")

        output = []

        for index, (key, value) in enumerate(data.items(), start=1):
            if isinstance(key, int):
                key = str(key)

            # handles single value/answer containing uuid and excludes uuid key
            # & display the value only.
            try:
                if isinstance(key, str) and uuid.UUID(key, version=4):
                    output.append(cls.format_values(value, index))

            # handles multiple nested values containing year, month formatting and others
            except:  # noqa
                if isinstance(value, list) and any(
                    isinstance(item, dict) for item in value
                ):
                    formatted_nested_values = cls.format_nested_data(value)
                    output.append(
                        f"{cls.indent(5)}. {key}: {formatted_nested_values}"
                        if index != 1
                        else f". {key}: {formatted_nested_values}"
                    )
                # handles all other multiple values
                else:
                    output.append(cls.format_keys_and_values(key, value, index))

        return output

    @classmethod
    def map_multi_input_data(cls, multi_input_data):
        """
        Map the multi-input data to a sorted dictionary and process it.

        Args:
            multi_input_data (list): The list of dictionaries representing the multi-input data.

        Returns:
            str: The processed output as a formatted string.
        """
        current_app.logger.info(
            f"[map_multi_input_data] processing data: {multi_input_data}"
        )

        try:
            sorted_data = {}
            for item in multi_input_data:
                if len(item) < 2:
                    for value in item.values():
                        key = str(uuid.uuid4())
                        sorted_data[key] = value
                else:
                    try:
                        key, *values = item.values()
                        sorted_data[key] = values
                    except TypeError:
                        value = tuple(item.values())
                        if isinstance(value[0], dict) and isinstance(value[1], str):
                            *values, key = item.values()
                            sorted_data[key] = values
                    except:  # noqa
                        print(
                            "Could not format the data correctly for"
                            f" {multi_input_data}"
                        )
                        key, *values = item.values()
                        sorted_data[json.dumps(key)] = values

            output = cls.process_data(sorted_data)
            return "\n".join(output)
        except Exception as e:
            current_app.logger.error(
                f"Error occurred while processing the multi input data: {e}"
            )
            current_app.logger.error(
                f"Couldn't map the multi input data for: {multi_input_data}"
            )
