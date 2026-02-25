from collections import defaultdict
from datetime import datetime
from decimal import Decimal
from io import BytesIO
from typing import Dict, List, Tuple, Union

from flask import Blueprint, render_template, request, send_file
from flask_login import login_required

from app.db import DatabaseManager
from app.utils import generate_report, permission_required

Tasks = List[Dict[str, Union[str, Decimal]]]
Data = List[List[Union[str, Decimal]]]

reports_bp: Blueprint = Blueprint("reports", __name__, url_prefix="/reports")
db_manager: DatabaseManager = DatabaseManager()


def does_period_contain_2025(start_date: datetime = None, end_date: datetime = None) -> bool:
    """
    Checks if the given period contains any date in the year 2025.

    Args:
        start_date (datetime, optional): The start of the period. Defaults to None.
        end_date (datetime, optional): The end of the period. Defaults to None.

    Returns:
        bool: True if the period includes any date in 2025, False otherwise.
    """
    lower_bound: datetime = datetime(2024, 12, 31)
    upper_bound: datetime = datetime(2026, 1, 1)

    if not start_date and not end_date:
        return True
    elif not start_date and end_date and end_date > lower_bound:
        return True
    elif start_date and end_date and lower_bound < start_date < upper_bound and end_date >= start_date:
        return True
    elif start_date and lower_bound < start_date < upper_bound and not end_date:
        return True
    return False


def get_tasks_data(tasks: Tasks) -> Data:
    """
    Converts tasks object into list of lists for report generation.

    Args:
        tasks (Tasks): List of task records, each containing employee details,
            order information, and work metrics.

    Returns:
        tasks_data (Data): List of lists, where each inner list contains the data for one specific task.
    """

    employee_categories: Dict[str, str] = {
        "worker": "Рабочий",
        "specialist": "Специалист",
        "manager": "Руководитель",
    }

    tasks_data: Data = [
        [
            task["employee_name"],
            task["personnel_number"],
            employee_categories[task["employee_category"]],
            task["department"],
            task["order_number"],
            task["order_name"],
            task["work_name"],
            task["hours"],
            task["operation_date"],
        ]
        for task in tasks
    ]
    return tasks_data


def get_employees_data(tasks: Tasks) -> Data:
    """
    Groups tasks by employee and date, summing hours for report generation.

    Creates unique key from employee details and date to aggregate hours,
    then formats the result with translated category names.

    Args:
        tasks (Tasks): List of task records, each containing employee details,
            order information, and work metrics.

    Returns:
        employees_data (Data):  List of lists, where each inner list contains the data for one specific employee
            on specific date.
    """

    spent_hours_by_employee: Dict[Tuple[str, ...], Decimal] = defaultdict(Decimal)

    for task in tasks:
        key: Tuple[str, ...] = (
            task["employee_name"],
            task["personnel_number"],
            task["employee_category"],
            task["department"],
            task["operation_date"],
        )
        spent_hours_by_employee[key] += task["hours"]

    employee_categories: Dict[str, str] = {
        "worker": "Рабочий",
        "specialist": "Специалист",
        "manager": "Руководитель",
    }

    employees_data: Data = [
        [
            key[0],
            key[1],
            employee_categories[key[2]],
            key[3],
            key[4],
            value,
        ]
        for key, value in spent_hours_by_employee.items()
    ]
    return employees_data


def get_orders_data(tasks: Tasks, start_date: datetime, end_date: datetime) -> Data:
    """
    Returns orders data including planned, spent, and remaining hours.

    This function calculates the total spent hours per order based on the provided tasks,
    optionally includes spent hours for the year 2025, if the specified date range requires it.

    Args:
        tasks (Tasks): List of task records, each containing employee details,
            order information, and work metrics.
        start_date (datetime): The start date for selecting tasks from the database.
        end_date (datetime): The end date for selecting tasks from the database.

    Returns:
        orders_data (Data): List of lists, where each inner list contains the data for one specific order,
            including its number, name, planned hours, spent hours, and remaining hours.
            The final inner list in the outer list contains the totals for planned hours, spent hours,
            and remaining hours calculated across all orders in the dataset.
    """

    spent_hours_by_order: Dict[str, Decimal] = defaultdict(Decimal)

    for task in tasks:
        spent_hours_by_order[task["order_number"]] += task["hours"]

    if does_period_contain_2025(start_date=start_date, end_date=end_date):
        spent_hours_for_2025: Dict[str, Decimal] = db_manager.orders.get_spent_hours_for_2025()

        for order_number, spent_hours in spent_hours_for_2025.items():
            spent_hours_by_order[order_number] += spent_hours

    orders_data: Data = []

    order_numbers: Tuple[str] = tuple(spent_hours_by_order.keys())

    if order_numbers:
        planned_hours_per_order: List = db_manager.orders.get_planned_hours_per_order(order_numbers)

        for order_number, order_name, planned_hours in planned_hours_per_order:
            spent_hours: Decimal = spent_hours_by_order[order_number]
            remaining_hours: Decimal = planned_hours - spent_hours
            orders_data.append(
                [
                    order_number,
                    order_name,
                    planned_hours,
                    spent_hours,
                    remaining_hours,
                ]
            )

    planned_hours, spent_hours, remaining_hours = Decimal(0), Decimal(0), Decimal(0)

    for order_data in orders_data:
        planned_hours += order_data[2]
        spent_hours += order_data[3]
        remaining_hours += order_data[4]

    orders_data.append(["ИТОГО", "", planned_hours, spent_hours, remaining_hours])
    return orders_data


@reports_bp.route("", methods=["GET"])
@login_required
@permission_required(["advanced"])
def reports() -> str:
    start_date: str = request.args.get("start_date")
    end_date: str = request.args.get("end_date")

    if start_date:
        start_date: Union[str, datetime] = datetime.strptime(start_date, "%Y-%m-%d")
    if end_date:
        end_date: Union[str, datetime] = datetime.strptime(end_date, "%Y-%m-%d")

    if request.args.get("export"):
        tasks: Tasks = db_manager.tasks.get_tasks(start_date=start_date, end_date=end_date)

        tasks_data: Data = get_tasks_data(tasks=tasks)
        employees_data: Data = get_employees_data(tasks=tasks)
        orders_data: Data = get_orders_data(tasks=tasks, start_date=start_date, end_date=end_date)

        file: BytesIO = generate_report(tasks_data, employees_data, orders_data)
        timestamp: str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        return send_file(file, download_name=f"{timestamp}.xlsx", as_attachment=True)

    return render_template("control/reports/generate_report.html")
