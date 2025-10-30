from flask import Blueprint, jsonify
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
    return jsonify(db_manager.employees.get_employees())
