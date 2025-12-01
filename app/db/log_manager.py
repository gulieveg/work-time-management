from typing import List, Tuple

from .db_connection import DatabaseConnection


class LogManager(DatabaseConnection):
    def get_logs(self) -> List[Tuple[str]]:
        query: str = "SELECT * FROM logs"

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                logs: List[Tuple[str]] = cursor.fetchall()
                return logs
