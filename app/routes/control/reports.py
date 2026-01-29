from decimal import Decimal
from typing import Dict, List, Union

from flask import Blueprint, render_template, request
from flask_login import login_required

from app.db import DatabaseManager
from app.utils import permission_required

Tasks = List[Dict[str, Union[str, Decimal]]]

reports_bp: Blueprint = Blueprint("reports", __name__, url_prefix="/reports")
db_manager: DatabaseManager = DatabaseManager()


@reports_bp.route("", methods=["GET"])
@login_required
@permission_required(["advanced"])
def generate_reports() -> str:
    args: Dict[str, str] = {
        "start_date": request.args.get("start_date"),
        "end_date": request.args.get("end_date"),
    }

    tasks: Tasks = db_manager.tasks.get_tasks(**args)
    return render_template("control/reports/generate_reports.html")
