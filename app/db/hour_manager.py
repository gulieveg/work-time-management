from decimal import Decimal
from typing import Any, Dict, List, Optional, Tuple, Union

from .db_connection import DatabaseConnection


class HourManager(DatabaseConnection):
    def add_hours(self, order_id: int, work_name: str, spent_hours: Decimal) -> None:
        query: str = """
            INSERT INTO hours (order_id, work_name, spent_hours)
            VALUES (?, ?, ?)
        """

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (order_id, work_name, spent_hours))
                connection.commit()

    def get_hours_list(self) -> List:
        query: str = "SELECT id, order_id, work_name, spent_hours FROM hours"

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                hours_list: List[Tuple[Any]] = cursor.fetchall()
                return hours_list
