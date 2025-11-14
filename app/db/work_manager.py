from decimal import Decimal
from typing import Dict, List, Union

from .db_connection import DatabaseConnection


class WorkManager(DatabaseConnection):
    def add_work_to_order(self, order_id: int, work_name: str, work_planned_hours: Decimal) -> None:
        query: str = "INSERT INTO works (order_id, name, planned_hours) VALUES (?, ?, ?)"

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (order_id, work_name, work_planned_hours))
                connection.commit()

    def work_exists(self, order_id: int, work_name: str) -> bool:
        query: str = "SELECT COUNT(*) FROM works WHERE order_id = ? AND name = ?"

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (order_id, work_name))
                count: int = cursor.fetchone()[0]
        return count > 0

    def get_works_for_order_by_id(self, order_id: int) -> List[Dict[str, Union[str, Decimal]]]:
        query: str = "SELECT id, name, planned_hours, spent_hours FROM works WHERE order_id = ?"

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (order_id,))

                works: List[Dict[str, Union[str, Decimal]]] = [
                    {
                        "work_id": work_data[0],
                        "work_name": work_data[1],
                        "planned_hours": work_data[2],
                        "spent_hours": work_data[3],
                    }
                    for work_data in cursor.fetchall()
                ]
                return works
        return count > 0

    def get_works_for_order_by_number(self, order_number: str) -> List[Dict[str, Union[str, Decimal]]]:
        query: str = """
            SELECT
                works.id,
                works.name,
                works.planned_hours,
                works.spent_hours
            FROM works
            JOIN orders ON works.order_id = orders.id
            WHERE orders.number = ?
        """

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (order_number,))

                works: List[Dict[str, Union[str, Decimal]]] = [
                    {
                        "work_id": work_data[0],
                        "work_name": work_data[1],
                        "planned_hours": work_data[2],
                        "spent_hours": work_data[3],
                    }
                    for work_data in cursor.fetchall()
                ]
                return works
