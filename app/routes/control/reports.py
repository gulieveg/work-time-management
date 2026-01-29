from flask import Blueprint, request
from flask_login import login_required

from app.db import DatabaseManager
from app.utils import permission_required

reports_bp: Blueprint = Blueprint("reports", __name__, url_prefix="/reports")
db_manager: DatabaseManager = DatabaseManager()


@reports_bp.route("", methods=["GET"])
@login_required
@permission_required(["advanced"])
def reports() -> str:
    start_date: str = request
