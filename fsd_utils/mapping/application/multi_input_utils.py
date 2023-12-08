import uuid

from fsd_utils.mapping.application.application_utils import number_to_month


class ProcessTypes:
    @classmethod
    def _str_single_item(cls, item: dict, sorted_data: dict) -> dict:
        """
        Convert a single item to a dictionary and append it to the sorted_data.

        Args:
            item (dict): A dictionary containing data.
            sorted_data (dict): A dictionary to store sorted data.

        Returns:
            dict: The updated sorted_data dictionary.
        """
        if len(item) < 2:
            for value in item.values():
                key = str(uuid.uuid4())
                sorted_data[key] = value
        if sorted_data:
            return sorted_data

    @classmethod
    def _dict_single_item(cls, item: dict, sorted_data: dict) -> dict:
        """
        Recursively processes a dictionary item to extract and validate date values.

        Args:
            item (dict): The dictionary item to process.
            sorted_data (dict): A dictionary to store sorted date values.

        Returns:
            dict: A dictionary containing validated date values.
        """
        for value in item.values():
            if isinstance(value, dict):
                date = cls.validated_iso_value(value)
                sorted_data[f"date_{str(uuid.uuid4())}"] = date
            elif isinstance(value, str):
                cls._str_single_item(item, sorted_data)
        if sorted_data:
            return sorted_data

    @classmethod
    def _dict_items(cls, item: dict, sorted_data: dict) -> dict:
        """
        Adds validated 'address' and 'value_str_len_two' items to a dictionary.

        This class method validates an 'item's address and checks if it has a two-item value string.
        If the address is valid, it is added to 'sorted_data' with a unique key.
        If 'value_str_len_two' is present, it is also added to 'sorted_data' with an appropriate key.
        If neither address nor 'value_str_len_two' are found, it sorts the dictionary items based on 'item'.

        Args:
            cls: The class reference.
            item: The item to be processed.
            sorted_data: The dictionary to which items are added.
        """
        address = cls.validate_address(item)
        if address:
            sorted_data[f"address_{str(uuid.uuid4())}"] = address

        value_len_two = cls.value_len_two(item)
        if value_len_two:
            sorted_data[value_len_two[0]] = value_len_two[1]

        if not address and not value_len_two:
            cls.sort_dict_items(item, sorted_data)

    @classmethod
    def sort_dict_items(cls, item: dict, sorted_data: dict) -> dict:
        """
        Sorts and updates a dictionary with a given item.

        Args:
            item: The item to be sorted and added to the dictionary.
            sorted_data: The dictionary to which the item will be added.

        Returns:
            dict: The updated dictionary with the sorted item.
        """

        _values, key = cls.value_len_greater_two(item)
        if len(_values) > 1:
            sorted_data[key] = _values
        else:
            sorted_data[key] = ", ".join(map(str, _values))

        if sorted_data:
            return sorted_data

    @classmethod
    def value_len_two(cls, item: dict) -> list:
        """
        Filters and returns a list of string values from a dictionary `item`
        if the dictionary has exactly two items and both values are strings.

        Parameters:
        - item (dict): The input dictionary to filter.

        Returns:
        - list: A list containing string values from the dictionary, or None if no such values are found.
        """
        _values = []
        if len(item) == 2:
            for value in item.values():
                if isinstance(value, (str, int)):
                    _values.append(value)
                if isinstance(value, dict):
                    date = cls.validated_iso_value(value)
                    if date:
                        _values.append(date)
                    address = cls.validate_address(value)
                    if address:
                        _values.append(address)
        if _values:
            return _values

    @classmethod
    def value_len_greater_two(cls, item: dict) -> tuple:
        """
        Extracts and combines values from a dictionary 'item' if its length is greater than 2.

        If 'item' contains dictionaries, it validates and appends ISO date values.
        If not, it combines string and integer values into a list along with a key.

        Args:
            item (dict): The dictionary to process.

        Returns:
            tuple: A tuple containing a list of combined values and the identified key, if available.
        """
        combined_values = []
        key = None
        if len(item) > 2:
            for value in item.values():
                if isinstance(value, dict):
                    date = cls.validated_iso_value(value)
                    if date:
                        combined_values.append(date)
                    address = cls.validate_address(value)
                    if address:
                        combined_values.append(address)
                    elif not date and not address:
                        dict_values = [
                            val
                            for val in value.values()
                            if val is not None and val != ""
                        ]
                        combined_values.append(", ".join(map(str, dict_values)))
                if isinstance(value, (str, int)):
                    _str_key = [
                        val for val in item.values() if isinstance(val, (str, int))
                    ]
                    if _str_key:
                        key = next(
                            (
                                item
                                for item in _str_key
                                if not isinstance(item, int) and item is not None
                            ),
                            _str_key[0],
                        )

        _values = [
            val for val in item.values() if val != key if not isinstance(val, dict)
        ]
        combined_values.extend(_values)

        if combined_values and key:
            return combined_values, key

    @classmethod
    def validated_iso_value(cls, value: dict) -> str:
        """
        Validates and converts ISO date components in 'value' dictionary to a formatted string.

        Args:
            value (dict): A dictionary containing ISO date components.

        Returns:
            str: A formatted string with valid date components, or None if no valid components found.
        """
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
    def validate_address(cls, item: dict) -> list:
        """
        Validates and extracts a complete address from a dictionary.

        This class method takes a dictionary 'item' and checks for specific address keys
        ("addressLine1", "addressLine2", "county", "postcode", "town") to extract a
        complete address. If valid address components are found, they are returned as a list.

        Args:
            item (dict): A dictionary containing address components.

        Returns:
            list: A list of valid address components in the order of ["addressLine1",
                  "addressLine2", "county", "postcode", "town"]. Returns an empty list if
                  no valid components are found.
        """
        address_keys = ["addressLine1", "addressLine2", "county", "postcode", "town"]
        address = []
        for key, value in item.items():
            if key in address_keys and value is not None and value != "":
                address.append(value)
        if address:
            return ", ".join(str(item) for item in address if item is not None)

    @classmethod
    def is_valid_uuid(cls, uuid_str: str) -> bool:
        """
        Check if a given string contains valid UUIDs separated by underscores.

        Args:
            uuid_str (str): The input string possibly containing UUIDs.

        Returns:
            bool: True if at least one valid UUID is found in the string, otherwise False.
        """

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
