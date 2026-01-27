from decimal import Decimal
from typing import Dict, List, Tuple, Union

from flask import Blueprint, Response, flash, redirect, render_template, request, url_for
from flask_login import login_required

from app.db import DatabaseManager
from app.utils import MESSAGES, permission_required

hours_bp: Blueprint = Blueprint("hours", __name__, url_prefix="/hours")
db_manager: DatabaseManager = DatabaseManager()


@hours_bp.route("/add", methods=["GET", "POST"])
@login_required
@permission_required(["advanced"])
def add_hours() -> Union[str, Response]:
    if request.method == "POST":
        order_number: str = request.form.get("order_number")
        work_name: str = request.form.get("work_name")
        spent_hours: str = request.form.get("spent_hours")

        order_id: int = db_manager.orders.get_order_id_by_number(order_number)

        db_manager.hours.add_hours(order_id, work_name, Decimal(spent_hours))

        flash(message=MESSAGES["hours"]["hours_added"], category="info")
        return render_template("control/hours/add_hours.html")
    return render_template("control/hours/add_hours.html")
