from collections import defaultdict
from datetime import datetime
from decimal import Decimal
from io import BytesIO
from typing import Dict, List, Optional, Tuple, Union

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

    if request.args.get("export"):
        tasks: Tasks = db_manager.tasks.get_tasks(start_date=start_date, end_date=end_date)

        spent_hours_by_order: Dict[str, Decimal] = defaultdict(Decimal)  # { "order_number": "spent_hours" }

        for task in tasks:
            spent_hours_by_order[task["order_number"]] += task["hours"]

        if not start_date or datetime.strptime(start_date, "%Y-%m-%d") < datetime(2026, 1, 1):
            spent_hours_by_order_2025: Dict[str, Decimal] = db_manager.orders.get_spent_hours_by_order_2025()

            for order_number, spent_hours in spent_hours_by_order_2025.items():
                spent_hours_by_order[order_number] += spent_hours

        grouped_data: List[List[Union[str, Decimal]]] = []

        order_numbers: Tuple[str] = tuple(spent_hours_by_order.keys())

        if order_numbers:
            orders_data: List[Union[str, Decimal]] = db_manager.orders.get_orders_data(order_numbers)

            for order_number, order_name, planned_hours in orders_data:
                spent_hours: Decimal = spent_hours_by_order[order_number]
                remaining_hours: Decimal = planned_hours - spent_hours
                grouped_data.append([order_number, order_name, planned_hours, spent_hours, remaining_hours])

        file: BytesIO = generate_report(grouped_data)
        filename: str = "report_{}.xlsx".format(today)
        return send_file(file, as_attachment=True, download_name=filename)

    return render_template("control/reports/generate_report.html")
