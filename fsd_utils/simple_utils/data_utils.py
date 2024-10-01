import requests
from flask import current_app


def get_remote_data_as_json(endpoint):
    response = requests.get(endpoint)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        current_app.logger.warning(
            "GET remote data call was unsuccessful with status code: %s body: %s.", response.status_code, response.text
        )
        response.raise_for_status()
