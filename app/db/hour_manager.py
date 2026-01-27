from decimal import Decimal
from typing import Any, List, Tuple

from .db_connection import DatabaseConnection


class HourManager(DatabaseConnection):
    def add_hours(self, order_name: str, order_number: str, spent_hours: Decimal) -> None:
        query: str = """
            INSERT INTO hours (order_name, order_number, spent_hours)
            VALUES (?, ?, ?)
        """

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (order_name, order_number, spent_hours))
                connection.commit()

    def delete_hours(self, hours_id: int) -> None:
        query: str = "DELETE FROM hours WHERE id = ?"

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (hours_id,))
                connection.commit()

    def get_hours_list(self) -> List:
        query: str = """
            SELECT id, order_name, order_number, spent_hours, created_date, created_time
            FROM hours
        """

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                hours_list: List[Tuple[Any]] = cursor.fetchall()
                return hours_list
