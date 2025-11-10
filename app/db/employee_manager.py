import re
from decimal import Decimal
from typing import List, Match, Optional, Tuple

from .db_connection import DatabaseConnection


class EmployeeManager(DatabaseConnection):
    def add_employee(self, name: str, personnel_number: str, department: str, operation_type: str) -> None:
        query: str = """
            IF NOT EXISTS (SELECT * FROM employees WHERE personnel_number = ?)
            INSERT INTO employees (name, department, personnel_number, operation_type)
            VALUES (?, ?, ?, ?)
        """

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (personnel_number, name, department, personnel_number, operation_type))
                connection.commit()

    def get_employee_used_hours(self, personnel_number: str, operation_date: str) -> Decimal:
        query: str = """
            SELECT SUM(hours)
            FROM tasks
            WHERE personnel_number = ? and operation_date = ?
        """

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (personnel_number, operation_date))
                used_hours: Decimal = cursor.fetchone()[0]

                if used_hours is None:
                    used_hours: Decimal = Decimal(0)
                return used_hours

    def get_employee_free_hours(self, personnel_number: str, operation_date: str) -> Decimal:
        hours_per_day: Decimal = Decimal(8.25)
        used_hours: Decimal = self.get_employee_used_hours(personnel_number, operation_date)
        return hours_per_day - used_hours

    def get_employee_operation_type(self, personnel_number: str) -> Optional[str]:
        query: str = "SELECT operation_type FROM employees WHERE personnel_number = ?"

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (personnel_number,))

                res: Optional[Tuple[str]] = cursor.fetchone()
                if res:
                    return res[0]

    def get_employee_department(self, personnel_number: str) -> Optional[str]:
        query: str = "SELECT department FROM employees WHERE personnel_number = ?"

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (personnel_number,))

                res: Optional[Tuple[str]] = cursor.fetchone()
                if res:
                    return res[0]

    def get_employee_category(self, personnel_number: str) -> Optional[str]:
        query: str = "SELECT category FROM employees WHERE personnel_number = ?"

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (personnel_number,))

                res: Optional[Tuple[str]] = cursor.fetchone()
                if res:
                    return res[0]

    def get_employees_by_partial_match(self, query: str) -> List[str]:
        query_string: str = """
            SELECT name, personnel_number
            FROM employees
            WHERE name LIKE ? OR personnel_number LIKE ?
        """

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query_string, ("%" + query + "%", "%" + query + "%"))
                employees = [f"{name} ({personnel_number})" for name, personnel_number in cursor.fetchall()]
                return employees

    def get_operation_types_by_partial_match(self, query: str) -> List[str]:
        query_string: str = """
            SELECT operation_type
            FROM employees
            WHERE operation_type LIKE ?
        """

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query_string, ("%" + query + "%",))

                operation_types: List[str] = []
                for data in cursor.fetchall():
                    if data[0] not in operation_types:
                        operation_types.append(data[0])
                return operation_types

    def get_work_types(self) -> List[str]:
        query: str = "SELECT name FROM work_types"

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)

                work_types: List[str] = []
                for data in cursor.fetchall():
                    if data[0] not in work_types:
                        work_types.append(data[0])
                return work_types

    def get_work_types_by_partial_match(self, query: str) -> List[str]:
        query_string: str = "SELECT name FROM work_types WHERE name LIKE ?"

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query_string, ("%" + query + "%",))

                work_types: List[str] = []
                for data in cursor.fetchall():
                    if data[0] not in work_types:
                        work_types.append(data[0])
                return work_types

    def does_employee_exist(self, personnel_number: str) -> bool:
        query: str = "SELECT * FROM employees WHERE personnel_number = ?"

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (personnel_number,))
                return cursor.fetchone() is not None

    def get_employee_details(self, employee_data: str) -> Optional[Tuple[str, str]]:
        pattern: str = "(?P<employee_name>[\\w\\s]+)\\s\\((?P<personnel_number>\\d+)\\)"
        matched: Match[str] = re.fullmatch(pattern=pattern, string=employee_data)
        if matched is None:
            return None
        return matched.group("employee_name"), matched.group("personnel_number")

    def get_total_employee_count(self) -> int:
        query: str = "SELECT COUNT(*) FROM employees"

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchone()[0]

    def get_departments(self) -> List[str]:
        query: str = "SELECT name FROM departments"

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)

                departments: List[str] = []
                for data in cursor.fetchall():
                    if data[0] not in departments:
                        departments.append(data[0])
                return departments

    def get_employees(
        self,
        employee_name: Optional[str] = None,
        employee_number: Optional[str] = None,
        page: Optional[int] = None,
    ) -> List[str]:
        query: str = """
            SELECT id, name, personnel_number, department, category
            FROM employees
        """

        conditions: List[str] = []
        params: List[str] = []

        if employee_name:
            conditions.append("name = ?")
            params.append(employee_name)
        if employee_number:
            conditions.append("personnel_number = ?")
            params.append(employee_number)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                if page:
                    page_size: int = 10
                    offset: int = (page - 1) * page_size
                    params.append(offset)
                    params.append(page_size)
                    query += "ORDER BY id OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"

                cursor.execute(query, tuple(params))
                employees: List[Tuple[str]] = cursor.fetchall()
                return employees

    def get_employee_names_by_partial_match(self, query: str) -> List[str]:
        query_string: str = "SELECT name FROM employees WHERE name LIKE ?"
        ...
