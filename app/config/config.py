from yaml import safe_load


def get_settings(config_file_name: str = "./app/config/config.yaml"):
    with open(config_file_name) as file:
        data = safe_load(file)
    return data


def get_db_url(config_file_name: str = "./app/config/config.yaml"):
    settings = get_settings(config_file_name)

    return f"postgresql://{settings['postgres_db']['user']}:" \
                        f"{settings['postgres_db']['password']}@" \
                        f"{settings['postgres_db']['host']}:" \
                        f"{settings['postgres_db']['port']}/" \
                        f"{settings['postgres_db']['db_name']}"
