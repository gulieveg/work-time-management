from decimal import Decimal
from io import BytesIO
from typing import Dict, List, Union

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
def report_docs() -> str:
    args: Dict[str, str] = {
        "start_date": request.args.get("start_date"),
        "end_date": request.args.get("end_date"),
    }

    tasks: Tasks = db_manager.tasks.get_tasks(**args)

    "SELECT "
    file: BytesIO = generate_report(tasks)
    return send_file(file, as_attachment=True, download_name="report.xlsx")
    return render_template("control/reports/generate_reports.html")
