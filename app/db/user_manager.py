import hashlib
from typing import Any, List, Optional, Tuple, Dict, Union

from .db_connection import DatabaseConnection


class UserManager(DatabaseConnection):
    def add_user(
        self,
        name: str,
        department: str,
        login: str,
        password: str,
        permissions_level: str,
        is_enabled: int,
        is_factory_worker: int,
    ) -> None:
        password_hash: Optional[str] = None

        if password and password.strip():
            password_hash: str = hashlib.sha256(password.encode()).hexdigest()

        query: str = """
            INSERT INTO users (
                name,
                department,
                login,
                password_hash,
                permissions_level,
                is_enabled,
                is_factory_worker
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    query, (name, department, login, password_hash, permissions_level, is_enabled, is_factory_worker)
                )
                connection.commit()

    def delete_user(self, user_id: int) -> None:
        query: str = "DELETE FROM users WHERE id = ?"

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (user_id,))
                connection.commit()

    def register_user(self, login: str, password: str) -> None:
        password_hash: str = hashlib.sha256(password.encode()).hexdigest()

        query: str = "UPDATE users SET password_hash = ? WHERE login = ?"

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (password_hash, login))
                connection.commit()

    def authenticate_user(self, login: str, password: str) -> bool:
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        query: str = "SELECT * FROM users WHERE login = ? AND password_hash = ?"

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (login, password_hash))
                return cursor.fetchone() is not None

    def is_user_existing(self, login: str) -> bool:
        query: str = "SELECT * FROM users WHERE login = ?"

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (login,))
                return cursor.fetchone() is not None

    def is_login_available(self, login: str) -> bool:
        query: str = "SELECT login FROM users WHERE login = ?"

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (login,))
                record: Optional[Tuple[str]] = cursor.fetchone()
                return bool(record and record[0])

    def is_user_enabled(self, login: str) -> int:
        query: str = "SELECT is_enabled FROM users WHERE login = ?"

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (login,))
                return cursor.fetchone()[0]

    def is_user_disabled(self, user_id: int) -> bool:
        query: str = "SELECT is_enabled FROM users WHERE id = ?"

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (user_id,))
                return not cursor.fetchone()[0]

    def is_user_registered(self, login: str) -> bool:
        query: str = "SELECT password_hash FROM users WHERE login = ?"

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (login,))
                record: Optional[Tuple[str]] = cursor.fetchone()
                return bool(record and record[0])

    def is_user_deleted(self, user_id: int) -> bool:
        query: str = "SELECT * FROM users WHERE id = ?"

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (user_id,))
                record: Optional[Tuple[Any, ...]] = cursor.fetchone()
                return record is None

    def update_user_status(self, user_id: int, is_active: bool) -> None:
        query: str = "UPDATE users SET is_enabled = ? WHERE id = ?"

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (is_active, user_id))
                connection.commit()

    def get_user_data_by_id(self, user_id: int) -> Optional[Dict[str, Union[str, int]]]:
        query: str = """
            SELECT id, name, department, login, permissions_level, is_factory_worker, is_enabled
            FROM users
            WHERE id = ?
        """

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (user_id,))

                user_data: Optional[Tuple[str]] = cursor.fetchone()
                print(user_data)
                if user_data:
                    return {
                        "user_id": user_data[0],
                        "user_name": user_data[1],
                        "user_department": user_data[2],
                        "user_login": user_data[3],
                        "user_permissions_level": user_data[4],
                        "is_user_factory_worker": user_data[5],
                        "is_user_account_enabled": user_data[6],
                    }

    def get_user_data_by_login(self, login: str) -> Optional[Dict[str, Union[str, int]]]:
        query: str = """
            SELECT id, name, login, department, permissions_level, is_factory_worker, is_enabled
            FROM users
            WHERE login = ?
        """

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (login,))

                user_data: Optional[Tuple[str]] = cursor.fetchone()
                if user_data:
                    return {
                        "user_id": user_data[0],
                        "user_name": user_data[1],
                        "user_department": user_data[2],
                        "user_login": user_data[3],
                        "user_permissions_level": user_data[4],
                        "is_user_factory_worker": user_data[5],
                        "is_user_account_enabled": user_data[6],
                    }

    def get_users(
        self,
        user_name: Optional[str] = None,
        user_login: Optional[str] = None,
        page: Optional[int] = None,
    ) -> List[Tuple[str]]:
        query: str = """
            SELECT id, name, login, department, permissions_level, is_enabled, is_factory_worker
            FROM users
        """

        conditions: List[str] = []
        params: List[str] = []

        if user_name:
            conditions.append("name = ?")
            params.append(user_name)
        if user_login:
            conditions.append("login = ?")
            params.append(user_login)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

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
                cursor.execute(query, tuple(params))
                users: List[Tuple[str]] = cursor.fetchall()
                return users

    def get_user_names_by_partial_match(self, query: str) -> List[str]:
        query_string: str = "SELECT name FROM users WHERE name LIKE ?"

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query_string, ("%" + query + "%",))
                user_names: List[str] = [data[0] for data in cursor.fetchall()]
                return user_names

    def get_user_logins_by_partial_match(self, query: str) -> List[str]:
        query_string: str = "SELECT login FROM users WHERE login LIKE ?"

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query_string, ("%" + query + "%",))
                user_logins: List[str] = [data[0] for data in cursor.fetchall()]
                return user_logins

    def get_user_name_by_login(self, user_login: str) -> Optional[str]:
        query: str = "SELECT name FROM users WHERE login = ?"

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (user_login,))

                row: Optional[Tuple[str]] = cursor.fetchone()
                return row and row[0]

    def get_user_login_by_name(self, user_name: str) -> Optional[str]:
        query: str = "SELECT login FROM users WHERE name = ?"

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (user_name,))

                row: Optional[Tuple[str]] = cursor.fetchone()
                return row and row[0]
