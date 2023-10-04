import uuid

from fsd_utils.mapping.application.application_utils import number_to_month


class ProcessTypes:
    @classmethod
    def _str_single_item(cls, item, sorted_data):
        if len(item) < 2:
            for value in item.values():
                key = str(uuid.uuid4())
                sorted_data[key] = value
        if sorted_data:
            return sorted_data

    @classmethod
    def _dict_single_item(cls, item, sorted_data):
        for value in item.values():
            if isinstance(value, dict):
                date = cls.validated_iso_value(value)
                sorted_data[f"date_{str(uuid.uuid4())}"] = date
            elif isinstance(value, str):
                cls._str_single_item(item, sorted_data)
        if sorted_data:
            return sorted_data

    @classmethod
    def validate_address(cls, item):
        address_keys = ["addressLine1", "addressLine2", "county", "postcode", "town"]
        address = []
        for key, value in item.items():
            if key in address_keys and value is not None and value != "":
                address.append(value)
        if address:
            return address

    @classmethod
    def _dict_items(cls, item, sorted_data):
        address = cls.validate_address(item)
        if address:
            sorted_data[f"address_{str(uuid.uuid4())}"] = ", ".join(address)

        value_str_len_two = cls.value_str_len_two(item)
        if value_str_len_two:
            sorted_data[value_str_len_two[0]] = value_str_len_two[1]

        if not address and not value_str_len_two:
            cls.sort_dict_items(item, sorted_data)

    @classmethod
    def value_str_len_two(cls, item):
        _values = []
        if len(item) == 2:
            for value in item.values():
                if isinstance(value, str):
                    _values.append(value)
        if _values:
            return _values

    @classmethod
    def value_str_len_greater_two(cls, item):
        combined_values = []
        key = None
        if len(item) > 2:
            for value in item.values():
                if isinstance(value, dict):
                    date = cls.validated_iso_value(value)
                    if date:
                        combined_values.append(date)
                    elif not date:
                        dict_values = [val for val in value.values()]
                        combined_values.append(", ".join(map(str, dict_values)))
                if isinstance(value, (str, int)):
                    _str_key = [
                        val for val in item.values() if isinstance(val, (str, int))
                    ]
                    if _str_key:
                        key = _str_key[0]

        _values = [
            val for val in item.values() if val != key if not isinstance(val, dict)
        ]
        combined_values.extend(_values)

        if combined_values and key:
            return combined_values, key

    @classmethod
    def sort_dict_items(cls, item, sorted_data):

        _values, key = cls.value_str_len_greater_two(item)
        if len(_values) > 1:
            sorted_data[key] = _values
        else:
            sorted_data[key] = ", ".join(map(str, _values))

        if sorted_data:
            return sorted_data

    @classmethod
    def validated_iso_value(cls, value):
        iso_keys = ["date", "month", "year"]
        date = []
        for k, v in value.items():
            key_split = k.split("__")
            if key_split:
                iso_keys_found = [n_key for n_key in key_split if n_key in iso_keys]
                if iso_keys_found:
                    month_name = number_to_month(
                        v,
                        *iso_keys_found,
                    )
                    date.append(month_name)
        if date:
            return " ".join(str(item) for item in date if item is not None)

    @classmethod
    def is_valid_uuid(cls, uuid_str):
        def is_valid_uuid_part(part):
            try:
                uuid.UUID(part, version=4)
                return True
            except ValueError:
                return False

        split_uuid_str = uuid_str.split("_")
        if any(part for part in split_uuid_str if is_valid_uuid_part(part)):
            return True

        return False
