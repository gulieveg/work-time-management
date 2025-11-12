from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Optional, Tuple, Union

from .db_connection import DatabaseConnection
from .employee_manager import EmployeeManager

Tasks = List[Dict[str, Union[str, Decimal]]]


class TaskManager(DatabaseConnection):
    def add_task(
        self,
        employee_name: str,
        personnel_number: str,
        department: str,
        operation_type: str,
        hours: Decimal,
        order_number: str,
        order_name: str,
        operation_date: str,
        employee_category: str,
    ) -> None:
        query: str = """
            INSERT INTO tasks (
                employee_name,
                personnel_number,
                department,
                operation_type,
                hours,
                order_number,
                order_name,
                operation_date,
                employee_category
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    query,
                    (
                        employee_name,
                        personnel_number,
                        department,
                        operation_type,
                        hours,
                        order_number,
                        order_name,
                        operation_date,
                        employee_category,
                    ),
                )
                connection.commit()

    def get_task_by_id(self, task_id: int) -> Optional[Dict[str, Union[str, Decimal]]]:
        query: str = """
            SELECT
                id,
                employee_name,
                personnel_number,
                department,
                operation_type,
                hours,
                order_number,
                order_name,
                operation_date
            FROM tasks WHERE id = ?
        """

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (task_id,))

                res: Optional[Tuple[str]] = cursor.fetchone()
                if res:
                    return {
                        "id": res[0],
                        "employee_name": res[1],
                        "personnel_number": res[2],
                        "department": res[3],
                        "operation_type": res[4],
                        "hours": res[5],
                        "order_number": res[6],
                        "order_name": res[7],
                        "operation_date": res[8].strftime("%Y-%m-%d"),
                    }

    def delete_task(self, task_id: str) -> None:
        query: str = "DELETE FROM tasks WHERE id = ?"

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (task_id,))
                connection.commit()

    def get_tasks(
        self,
        departments: List[str],
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        employee_data: Optional[str] = None,
        order_number: Optional[str] = None,
        operation_type: Optional[str] = None,
        order_name: Optional[str] = None,
    ) -> Tasks:
        base_query: str = """
            SELECT id,
                employee_name,
                personnel_number,
                department,
                operation_type,
                hours,
                order_number,
                order_name,
                operation_date,
                employee_category
            FROM tasks
        """

        departments: List[str] = list(filter(None, departments))

        if departments:
            placeholders: str = ", ".join(["?"] * len(departments))
            query: str = f"{base_query} WHERE department IN ({placeholders})"
            params: List[str] = departments
        else:
            query: str = f"{base_query} WHERE 0 = 0"
            params: List[str] = []

        if start_date:
            query += " AND operation_date >= ?"
            params.append(start_date)

        if end_date:
            query += " AND operation_date <= ?"
            params.append(end_date)

        if not start_date and not end_date:
            query += " AND operation_date = ?"
            params.append(datetime.now().strftime("%Y-%m-%d"))

        if employee_data:
            employee_details: Optional[Tuple[str, str]] = EmployeeManager().get_employee_details(employee_data)
            if employee_details is None:
                query += " AND employee_name = ?"
                params.append(employee_data)
            else:
                _, personnel_number = employee_details
                query += " AND personnel_number = ?"
                params.append(personnel_number)

        if order_number:
            query += " AND order_number = ?"
            params.append(order_number)

        if operation_type:
            query += " AND operation_type = ?"
            params.append(operation_type)

        if order_name:
            query += " AND order_name = ?"
            params.append(order_name)

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, tuple(params))

                tasks: List[Dict[str, str]] = [
                    {
                        "id": task[0],
                        "employee_name": task[1],
                        "personnel_number": task[2],
                        "department": task[3],
                        "operation_type": task[4],
                        "hours": task[5],
                        "order_number": task[6],
                        "order_name": task[7],
                        "operation_date": task[8].strftime("%Y-%m-%d"),
                        "employee_category": task[9],
                    }
                    for task in cursor.fetchall()
                ]
                return tasks

    def update_task(
        self,
        task_id: int,
        employee_name: str,
        personnel_number: str,
        hours: Decimal,
        order_name: str,
        order_number: str,
        operation_date: str,
        operation_type: Optional[str] = None,
    ) -> None:
        department: str = EmployeeManager().get_employee_department(personnel_number)

        if operation_type is None:
            operation_type: str = EmployeeManager().get_employee_operation_type(personnel_number)

        query: str = """
            UPDATE tasks
            SET
                employee_name = ?,
                personnel_number = ?,
                department = ?,
                operation_type = ?,
                hours = ?,
                order_number = ?,
                order_name = ?,
                operation_date = ?
            WHERE id = ?
        """

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    query,
                    (
                        employee_name,
                        personnel_number,
                        department,
                        operation_type,
                        hours,
                        order_number,
                        order_name,
                        operation_date,
                        task_id,
                    ),
                )
                connection.commit()

    def get_total_task_count(self) -> int:
        query: str = "SELECT COUNT(*) FROM tasks"

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchone()[0]
