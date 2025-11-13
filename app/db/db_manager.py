from typing import List, Optional, Union

from .db_connection import DatabaseConnection
from .employee_manager import EmployeeManager
from .order_manager import OrderManager
from .task_manager import TaskManager
from .user_manager import UserManager
from .work_manager import WorkManager


class DatabaseManager(DatabaseConnection):
    def __init__(self):
        self.employees: EmployeeManager = EmployeeManager()
        self.orders: OrderManager = OrderManager()
        self.tasks: TaskManager = TaskManager()
        self.users: UserManager = UserManager()
        self.works: WorkManager = WorkManager()

    def fetch_column(
        self, column: str, table: str, where_column: str, value: str, multiple: bool = False
    ) -> Optional[Union[List[str], str]]:
        if multiple:
            query: str = f"SELECT {column} FROM {table} WHERE {where_column} LIKE ?"
            param: str = f"%{value}%"
        else:
            query: str = f"SELECT {column} FROM {table} WHERE {where_column} = ?"
            param: str = value

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (param,))
                if multiple:
                    return [row[0] for row in cursor.fetchall()]
                else:
                    res = cursor.fetchone()
                    return res[0] if res else None
