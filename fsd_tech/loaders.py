import importlib

from yaml import safe_load


def object_loader(object_path):
    path_list = object_path.rsplit(".", 1)
    module_path = path_list[0]
    class_name = path_list[1]

    imported_object = importlib.import_module(module_path)
    # Grabs the class from the module.
    import_class = getattr(imported_object, class_name)

    raw_dict = import_class.__dict__
    # Throws away any python generated attributes.
    processed_dict = {
        k: v
        for k, v in raw_dict.items()
        if not k.startswith("_") and not k.endswith("_")
    }

    return processed_dict


def yaml_loader(path):
    with open(path, "r") as stream:
        return_dict = safe_load(stream)
    return return_dict
