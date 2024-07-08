import configparser
from typing import Tuple

from flask import jsonify
from flask.wrappers import Response


def create_response(
    data: dict = None, status: int = 200, message: str = ""
) -> Tuple[Response, int]:
    if type(data) is not dict and data is not None:
        raise TypeError("Data should be a dictionary 😞")

    response = {"success": 200 <= status < 300, "message": message, "result": data}
    return jsonify(response), status

def all_exception_handler(error: Exception) -> Tuple[Response, int]:
    return create_response(message=str(error), status=500)

    """Gets Postgres URL including credentials from specified file.

    Example of File:
    ```
    [pg_creds]
    pg_url = postgresql://testusr:password@127.0.0.1:5432/testdb
    ```
    :param file name
    :returns str or None if exception failed
    """
    try:

        config = configparser.ConfigParser()
        config.read(file)

        mongo_section = config["pg_creds"]
        return mongo_section["pg_url"]
    except KeyError:
        print(
            f"Failed to retrieve postgres url. Check if {file} exists in the top directory and whether it follows the correct format. INGORE this message if you are not using {file} to store your credentials."
        )
        return None
