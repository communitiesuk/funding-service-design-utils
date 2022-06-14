from fsd_tech import load_config

if __name__ == "__main__":

    def adds_value(config_dict):

        config_dict["test"] = "hello"

        config_dict["new"] = "I Am made by post hook"

        return config_dict

    config = load_config(
        "example_config_folder/.env.default.example",
        "example_config_folder/.env.development.example",
        "example_config_folder.dev_config.dev_config",
        "example_config_folder/.talisman.test.yaml",
        post_hook=adds_value,
    )
