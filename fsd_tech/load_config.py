import itertools
import os
from collections.abc import Callable
from os import environ
from pathlib import Path
from typing import List

from dotenv import dotenv_values
from termcolor import colored
from termcolor import HIGHLIGHTS

from .config_borg import Config
from .loaders import object_loader
from .loaders import yaml_loader


def pretty_print_config_metadata(paths, meta_data_dict: dict, log_length=100):

    # Data used for pretty printing the configuration.
    background_colors = list(HIGHLIGHTS.keys())[1:-1]
    colour_dict = {
        k: v for k, v in zip(paths, itertools.cycle(background_colors))
    }
    colour_dict["Shell Env"] = "on_magenta"
    colour_dict["POST HOOK"] = "on_grey"

    for k, v in meta_data_dict.items():
        fmt_string_kv = f"{k} = {v['value']}"
        fmt_string_kv = fmt_string_kv.ljust(log_length, "-")
        coloured_altered = ""
        if v["post_hook_modified"]:
            coloured_altered = colored(
                "!!!ALTERED BY POST HOOK!!!", "red", "on_grey"
            )
        fmt_string_from = coloured_altered + colored(
            f"FROM {v['path']}", "white", colour_dict[v["path"]]
        )
        fmt_string = fmt_string_kv + fmt_string_from
        print(fmt_string)


def load_config(
    *paths: List[Path],
    post_hook: Callable[[dict], dict] | None = None,
    pretty_print=True,
    log_length=100,
):

    # A list of the loaded env files + some metadata about them.
    config_info_list = []

    # These sets will keep track of what set various keys.
    keys_from_files = set()

    for env_path in paths:

        if env_path.endswith((".yaml", ".yml")):
            env_dict = yaml_loader(env_path)

        elif ".env" in env_path:
            env_dict = dotenv_values(env_path)

        elif not os.path.exists(env_path) and "." in env_path:
            env_dict = object_loader(env_path)

        else:
            raise ValueError(f"Invalid config path given : {env_path}")

        env_dict_data_dict = {
            k: {"value": v, "path": str(env_path), "post_hook_modified": False}
            for k, v in env_dict.items()
        }

        keys_from_files.update(env_dict.keys())
        config_info_list.append(env_dict_data_dict)

    os_environ_dict = {
        k: {"value": v, "path": "Shell Env", "post_hook_modified": False}
        for k, v in environ.items()
        if k in keys_from_files
    }

    config_info_list.append(os_environ_dict)

    # Values are overwritten in the following order: files, Shell Envs.
    settled_metadata_dict = {}
    for config_dict in config_info_list:
        for k, v in config_dict.items():
            settled_metadata_dict[k] = v

    pre_hook_config = {}
    for k, v in settled_metadata_dict.items():
        pre_hook_config[k] = v["value"]

    if post_hook:

        post_hook_config = post_hook(pre_hook_config.copy())

        shared_keys = set.intersection(
            set(post_hook_config.keys()), set(pre_hook_config.keys())
        )

        new_keys = set(post_hook_config.keys() - pre_hook_config.keys())

        altered_keys = [
            k
            for k in shared_keys
            if not pre_hook_config[k] == post_hook_config[k]
        ]

        created_by_post_hook = {
            k: {
                "value": post_hook_config[k],
                "path": "POST HOOK",
                "post_hook_modified": False,
            }
            for k in new_keys
        }
        settled_metadata_dict.update(created_by_post_hook)

        for altered_key in altered_keys:
            settled_metadata_dict[altered_key]["value"] = post_hook_config[
                altered_key
            ]
            settled_metadata_dict[altered_key]["post_hook_modified"] = True

        return_dict = post_hook_config

    else:

        return_dict = pre_hook_config

    if pretty_print:

        pretty_print_config_metadata(
            paths, settled_metadata_dict, log_length=log_length
        )

    # Sets the singleton (actually borg) objects attributes to our dictionary
    Config().__dict__.update(return_dict)

    return return_dict
