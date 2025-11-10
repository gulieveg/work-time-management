from typing import Dict, List, Tuple, Union

from flask import Blueprint, jsonify, render_template, request
from flask_login import login_required
from werkzeug.wrappers import Response

from app.db import DatabaseManager
from app.utils import permission_required

employees_bp: Blueprint = Blueprint("employees", __name__, url_prefix="/employees")
db_manager: DatabaseManager = DatabaseManager()


@employees_bp.route("/", methods=["GET"])
@login_required
@permission_required(["advanced"])
def employees_table() -> Response:
    employee_name: str = request.form.get("employee_name")
    employee_number: str = request.form.get("employee_number")

    args: Dict[str, str] = {
        "employee_name": employee_name,
        "employee_number": employee_number,
    }

    filtered_employees: List[Tuple[str]] = db_manager.employees.get_employees(**args)
    if not filtered_employees:
        return render_template("control/employees/employees_table.html")

    page: int = request.args.get("page", 1, int)

    args: Dict[str, Union[str, int]] = {
        "employee_name": employee_name,
        "employee_number": employee_number,
        "page": page,
    }

    filtered_employees_page: List[Tuple[str]] = db_manager.employees.get_employees(**args)

    context: Dict[str, Union[int, List[Tuple[str]]]] = {
        "filtered_employees": filtered_employees,
        "filtered_employees_page": filtered_employees_page,
        "page": page,
    }
    return render_template("control/employees/employees_table.html", **context)
