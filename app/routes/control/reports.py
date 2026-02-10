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

reports_bp: Blueprint = Blueprint("reports", __name__, url_prefix="/reports")
db_manager: DatabaseManager = DatabaseManager()


@reports_bp.route("", methods=["GET"])
@login_required
@permission_required(["advanced"])
def reports() -> str:
    start_date: str = request.args.get("start_date")
    end_date: str = request.args.get("end_date")

    today: str = datetime.today().strftime("%Y-%m-%d")

    if start_date:
        start_date: Union[str, datetime] = datetime.strptime(start_date, "%Y-%m-%d")
    if end_date:
        end_date: Union[str, datetime] = datetime.strptime(end_date, "%Y-%m-%d")

    is_date_range_valid: bool = False

    lower_bound: datetime = datetime(2024, 12, 31)
    upper_bound: datetime = datetime(2026, 1, 1)

    if not start_date and not end_date:
        is_date_range_valid = True
    elif not start_date and end_date and end_date > lower_bound:
        is_date_range_valid = True
    elif start_date and end_date and lower_bound < start_date < upper_bound and end_date >= start_date:
        is_date_range_valid = True
    elif start_date and lower_bound < start_date < upper_bound and not end_date:
        is_date_range_valid = True

    if request.args.get("export"):
        tasks: Tasks = db_manager.tasks.get_tasks(start_date=start_date, end_date=end_date)

        spent_hours_by_order: Dict[str, Decimal] = defaultdict(Decimal)  # key: order_number, value: spent_hours

        for task in tasks:
            spent_hours_by_order[task["order_number"]] += task["hours"]

        if is_date_range_valid:
            spent_hours_by_order_2025: Dict[str, Decimal] = db_manager.orders.get_spent_hours_by_order_2025()

            for order_number, spent_hours in spent_hours_by_order_2025.items():
                spent_hours_by_order[order_number] += spent_hours

        grouped_orders_data: List[List[Union[str, Decimal]]] = []

        order_numbers: Tuple[str] = tuple(spent_hours_by_order.keys())

        if order_numbers:
            orders_data: List[Union[str, Decimal]] = db_manager.orders.get_orders_data(order_numbers)

            for order_number, order_name, planned_hours in orders_data:
                spent_hours: Decimal = spent_hours_by_order[order_number]
                remaining_hours: Decimal = planned_hours - spent_hours
                order_data: List[Union[str, Decimal]] = [
                    order_number,
                    order_name,
                    planned_hours,
                    spent_hours,
                    remaining_hours,
                ]
                grouped_orders_data.append(order_data)

        planned_hours, spent_hours, remaining_hours = Decimal(0), Decimal(0), Decimal(0)

        for order_data in grouped_orders_data:
            planned_hours += order_data[2]
            spent_hours += order_data[3]
            remaining_hours += order_data[4]

        grouped_orders_data.append(["ИТОГО", "", planned_hours, spent_hours, remaining_hours])

        employee_categories: Dict[str, str] = {
            "worker": "Рабочий",
            "specialist": "Специалист",
            "manager": "Ведущий специалист",
        }

        tasks_data: List[List[Union[str, Decimal]]] = [
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

        aggregated_hours: defaultdict = defaultdict(Decimal)

        for task in tasks:
            key = (
                task["employee_name"],
                task["personnel_number"],
                task["employee_category"],
                task["department"],
                task["operation_date"],
            )
            aggregated_hours[key] += task["hours"]

        employees_data: List[List[Union[str, Decimal]]] = [
            [
                key[0],
                key[1],
                employee_categories[key[2]],
                key[3],
                key[4],
                value,
            ]
            for key, value in aggregated_hours.items()
        ]

        print(employees_data)

        file: BytesIO = generate_report(tasks_data, employees_data, grouped_orders_data)
        return send_file(file, as_attachment=True, download_name=f"{today}.xlsx")

    return render_template("control/reports/generate_report.html")
