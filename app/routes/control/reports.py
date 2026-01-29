from datetime import datetime
from decimal import Decimal
from io import BytesIO
from typing import Dict, List, Optional, Union

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
    args: Dict[str, Optional[str]] = {
        "start_date": request.args.get("start_date"),
        "end_date": request.args.get("end_date"),
    }

    tasks: Tasks = db_manager.tasks.get_tasks(**args)

    # {
    #     "id": task[0],
    #     "employee_name": task[1],
    #     "personnel_number": task[2],
    #     "department": task[3],
    #     "work_name": task[4],
    #     "hours": task[5],
    #     "order_number": task[6],
    #     "order_name": task[7],
    #     "operation_date": task[8].strftime("%Y-%m-%d"),
    #     "employee_category": task[9],
    # }

    # file: BytesIO = generate_report(tasks)
    # return send_file(file, as_attachment=True, download_name="report.xlsx")

    today: str = datetime.today().strftime("%Y-%m-%d")
    context: Dict[str, str] = {
        "today": today,
    }
    return render_template("control/reports/generate_report.html", **context)
