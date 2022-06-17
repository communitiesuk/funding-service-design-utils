import os


def configclass(cls):

    # Checks base classes for _config_info_, a dict containing
    # all infomation about config. attrs, and
    # adds them to a list.
    config_infos = [
        base.__dict__["_config_info_"]
        for base in cls.__bases__
        if "_config_info_" in base.__dict__
    ]

    # We compile all of these _config_info_'s into a dictionary,
    #  with overwritten values.
    settled_bases_config_info = {
        k: v for config_dict in config_infos for k, v in config_dict.items()
    }

    # We extract the values from the class and overlay
    #  the above dict with its values.
    for k, v in cls.__dict__.items():
        if not (k.startswith("__") or k.endswith("__")):
            settled_bases_config_info[k] = {
                "value": v,
                "from": cls.__qualname__,
            }

    # This is the dicitonary that will be used
    #  by classes which inherit this class
    cls._config_info_ = settled_bases_config_info

    @classmethod
    def as_config_dict(cls):
        return {k: v["value"] for k, v in cls._config_info_.items()}

    @classmethod
    def pretty_print(self, print_values=False):

        if os.environ.get("FLASK_ENV") in ["development", "test", "dev"]:

            from rich.table import Table
            from rich.console import Console

            table = Table(title="Config Info", show_lines=True)

            table.add_column(
                "Key", justify="right", style="cyan", no_wrap=True
            )
            if print_values:
                table.add_column("Value", style="magenta", overflow="ellipsis")
            table.add_column("From", justify="right", style="green")

            for k, v in self._config_info_.items():
                config_key = str(k)
                config_value = str(v["value"])
                from_value = str(v["from"])
                if print_values:
                    table.add_row(config_key, config_value, from_value)
                else:
                    table.add_row(config_key, from_value)

            console = Console()
            console.print(table)

    cls.as_config_dict = as_config_dict

    cls.pretty_print = pretty_print

    return cls


if __name__ == "__main__":

    @configclass
    class Default:

        my_val = 1
        my_val_2 = 5

    @configclass
    class Dev(Default):

        my_val_2 = 10

    Dev.pretty_print()
