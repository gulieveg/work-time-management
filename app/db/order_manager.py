from typing import Dict, List, Optional, Tuple, Union

from .db_connection import DatabaseConnection


class OrderManager(DatabaseConnection):
    def add_order(self, order_number: str, order_name: str) -> None:
        query: str = """
            IF NOT EXISTS (SELECT * FROM orders WHERE number = ?)
            INSERT INTO orders (number, name)
            VALUES (?, ?)
        """

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (order_number, order_number, order_name))
                connection.commit()

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

    def get_order_by_id(self, order_id: int) -> Optional[Dict[str, Union[str, int]]]:
        query: str = "SELECT id, number, name FROM orders WHERE id = ?"

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (order_id,))

                res: Optional[Tuple[str]] = cursor.fetchone()
                if res:
                    return {
                        "id": res[0],
                        "order_number": res[1],
                        "order_name": res[2],
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
