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
    for k in cls.__dict__:
        if not (k.startswith("__") or k.endswith("__")):
            settled_bases_config_info[k] = cls.__qualname__

    # This is the dicitonary that will be used
    #  by classes which inherit this class
    cls._config_info_ = settled_bases_config_info

    @classmethod
    def pretty_print(self):

        from rich.table import Table
        from rich.console import Console

        table = Table(title="Config Info", show_lines=True)

        table.add_column("Key", justify="right", style="cyan", no_wrap=True)

        table.add_column("From", justify="right", style="yellow", no_wrap=True)

        for k, v in self._config_info_.items():
            config_key = str(k)
            from_value = str(v)
            table.add_row(config_key, from_value)

        console = Console()
        console.print(table)

    cls.pretty_print = pretty_print

    return cls
