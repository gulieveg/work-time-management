from collections import defaultdict
from decimal import Decimal
from typing import Dict, List, Optional, Tuple, Union

from .db_connection import DatabaseConnection


class OrderManager(DatabaseConnection):
    def add_order(self, order_number: str, order_name: str) -> int:
        query: str = "INSERT INTO orders (number, name) OUTPUT INSERTED.id VALUES (?, ?)"

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (order_number, order_name))
                order_id: int = cursor.fetchone()[0]
                connection.commit()
        return order_id

    def order_exists(self, order_number: str, exclude_id: Optional[int] = None) -> bool:
        query: str = "SELECT * FROM orders WHERE number = ?"

        params: List[str] = [order_number]

        if exclude_id is not None:
            query += " AND id <> ?"
            params.append(exclude_id)

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, tuple(params))
                record: Optional[Tuple[str]] = cursor.fetchone()
                return record is not None

    def get_order_names_by_partial_match(self, query: str) -> List[str]:
        query_string: str = "SELECT name FROM orders WHERE name LIKE ?"

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query_string, ("%" + query + "%",))
                order_names: List[str] = [data[0] for data in cursor.fetchall()]
                return order_names

    def get_order_numbers_by_partial_match(self, query: str) -> List[str]:
        query_string: str = "SELECT number FROM orders WHERE number LIKE ?"

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query_string, ("%" + query + "%",))
                order_numbers: List[str] = [data[0] for data in cursor.fetchall()]
                return order_numbers

    def get_order_number_by_name(self, order_name: str) -> Optional[str]:
        query: str = "SELECT number FROM orders WHERE name = ?"

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (order_name,))

                res: Optional[Tuple[str]] = cursor.fetchone()
                if res:
                    return res[0]

    def get_order_name_by_number(self, order_number: str) -> Optional[str]:
        query: str = "SELECT name FROM orders WHERE number = ?"

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (order_number,))

                res: Optional[Tuple[str]] = cursor.fetchone()
                if res:
                    return res[0]

    def get_order_id_by_number(self, order_number: str) -> Optional[int]:
        query: str = "SELECT id FROM orders WHERE number = ?"

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (order_number,))

                res: Optional[Tuple[str]] = cursor.fetchone()
                if res:
                    return res[0]

    def get_order_data_by_id(self, order_id: int) -> Optional[Dict[str, Union[str, int]]]:
        query: str = "SELECT id, number, name FROM orders WHERE id = ?"

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (order_id,))

                order_data: Optional[Tuple[str]] = cursor.fetchone()
                if order_data:
                    return {
                        "id": order_data[0],
                        "order_number": order_data[1],
                        "order_name": order_data[2],
                    }

    def delete_order(self, order_id: str) -> None:
        query: str = "DELETE FROM orders WHERE id = ?"

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (order_id,))
                connection.commit()

    def update_order(self, order_id: int, order_number: str, order_name: str) -> None:
        query: str = "UPDATE orders SET number = ?, name = ? WHERE id = ?"

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (order_number, order_name, order_id))
                connection.commit()

    def get_orders(
        self,
        order_number: Optional[str] = None,
        order_name: Optional[str] = None,
        page: Optional[int] = None,
    ) -> List[Tuple[str]]:
        query: str = """
            SELECT id, number, name
            FROM orders
            WHERE (? IS NULL OR ? = '' OR number = ?)
            AND (? IS NULL OR ? = '' OR name = ?)
        """

        params: List[str] = [order_number] * 3 + [order_name] * 3

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                if page:
                    page_size: int = 10
                    offset: int = (page - 1) * page_size
                    params.append(offset)
                    params.append(page_size)
                    query += """
                        ORDER BY id
                        OFFSET ? ROWS
                        FETCH NEXT ? ROWS ONLY
                    """
                cursor.execute(query, (tuple(params)))
                orders: List[Tuple[str]] = cursor.fetchall()
                return orders

    def get_total_order_count(self) -> int:
        query: str = "SELECT COUNT(*) FROM orders"

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchone()[0]

    def get_spent_hours_for_order_2025(self, order_number: str) -> Decimal:
        query: str = "SELECT spent_hours FROM hours WHERE order_number = ?"

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (order_number,))
                return cursor.fetchone()[0]

    def get_spent_hours_by_order_2025(self) -> Dict[str, Decimal]:
        query: str = "SELECT order_number, spent_hours FROM hours"

        spent_hours_by_order: Dict[str, Decimal] = defaultdict(Decimal)

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                for order_number, spent_hours in cursor.fetchall():
                    spent_hours_by_order[order_number] = spent_hours
                return spent_hours_by_order

    def get_planned_hours_for_order(self, order_number: str) -> Decimal:
        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                query: str = "SELECT id FROM orders WHERE number = ?"
                cursor.execute(query, (order_number,))
                order_id: int = cursor.fetchone()[0]

                query: str = "SELECT SUM(planned_hours) FROM works WHERE order_id = ?"
                cursor.execute(query, (order_id,))
                return cursor.fetchone()[0]

    def get_orders_data(self, order_numbers: Tuple[str]) -> List[Union[str, Decimal]]:
        query: str = f"""
            SELECT
                orders.number,
                orders.name,
                COALESCE(SUM(works.planned_hours), 0) AS planned_hours
            FROM orders
            LEFT JOIN works ON works.order_id = orders.id
            WHERE orders.number IN ({", ".join("?" for _ in order_numbers)})
            GROUP BY orders.number, orders.name
        """

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, order_numbers)
                orders_data: List[Union[str, Decimal]] = cursor.fetchall()
                return orders_data
