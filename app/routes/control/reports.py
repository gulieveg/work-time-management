from flask import Blueprint, render_template, request
from flask_login import login_required

from app.db import DatabaseManager
from app.utils import permission_required

reports_bp: Blueprint = Blueprint("reports", __name__, url_prefix="/reports")
db_manager: DatabaseManager = DatabaseManager()


@reports_bp.route("", methods=["GET"])
@login_required
@permission_required(["advanced"])
def generate_reports() -> str:
    start_date: str = request.form.get("start_date")
    end_date: str = request.form.get("end_date")
    return render_template("control/reports/generate_reports.html")
