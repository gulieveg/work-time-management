from decimal import Decimal
from typing import Any, List, Tuple

from .db_connection import DatabaseConnection


class HourManager(DatabaseConnection):
    def add_hours(self, order_id: int, work_name: str, spent_hours: Decimal) -> None:
        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                query: str = """
                    INSERT INTO hours (order_id, work_name, spent_hours)
                    VALUES (?, ?, ?)
                """
                cursor.execute(query, (order_id, work_name, spent_hours))

                query: str = """
                    UPDATE works
                    SET spent_hours = spent_hours + ?
                    WHERE order_id = ? AND name = ?
                """
                cursor.execute(query, (spent_hours, order_id, work_name))
            connection.commit()

    def delete_hours(self, hours_id: int) -> None:
        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                query: str = "SELECT order_id, work_name, spent_hours FROM hours WHERE id = ?"
                cursor.execute(query, (hours_id,))

                order_id, work_name, spent_hours = cursor.fetchone()

                query: str = """
                    UPDATE works
                    SET spent_hours = spent_hours - ?
                    WHERE order_id = ? AND name = ?
                """
                cursor.execute(query, (spent_hours, order_id, work_name))

                query: str = "DELETE FROM hours WHERE id = ?"
                cursor.execute(query, (hours_id,))
            connection.commit()

    def get_hours_list(self) -> List:
        query: str = "SELECT id, order_id, work_name, spent_hours, created_date, created_time FROM hours"

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                hours_list: List[Tuple[Any]] = cursor.fetchall()
                return hours_list
