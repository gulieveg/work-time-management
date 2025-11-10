from typing import Dict

import pyodbc
from decouple import config

from app.utils import encoding


class DatabaseConnection:
    def get_connection(self) -> pyodbc.Connection:
        db_config: Dict[str, str] = {
            "DRIVER": encoding.decode_base64(config("DATABASE_DRIVER")),
            "SERVER": encoding.decode_base64(config("DATABASE_SERVER")),
            "DATABASE": encoding.decode_base64(config("DATABASE_NAME")),
            "UID": encoding.decode_base64(config("DATABASE_USER")),
            "PWD": encoding.decode_base64(config("DATABASE_PASSWORD")),
        }
        connection_string: str = (
            f"DRIVER={db_config['DRIVER']};"
            f"SERVER={db_config['SERVER']};"
            f"DATABASE={db_config['DATABASE']};"
            f"UID={db_config['UID']};"
            f"PWD={db_config['PWD']};"
        )
        connection: pyodbc.Connection = pyodbc.connect(connection_string)
        return connection
