from typing import Dict

from flask import Blueprint, render_template
from flask_login import current_user, login_required

from app.db import DatabaseManager
from app.utils import permission_required

dashboard_bp: Blueprint = Blueprint("dashboard", __name__)
db_manager: DatabaseManager = DatabaseManager()


@dashboard_bp.route("/overview", methods=["GET"])
@login_required
@permission_required(["advanced"])
def overview() -> str:
    context: Dict[str, int] = {
        "user_name": current_user.name,
        "total_orders": db_manager.orders.get_total_order_count(),
        "total_employees": db_manager.employees.get_total_employee_count(),
        "total_tasks": db_manager.tasks.get_total_task_count(),
    }
    return render_template("control/dashboard/dashboard.html", **context)
