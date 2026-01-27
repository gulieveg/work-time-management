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
        spent_hours: str = request.form.get("spent_hours")

        order_name: str = db_manager.orders.get_order_name_by_number(order_number)

        db_manager.hours.add_hours(order_name, order_number, Decimal(spent_hours))

        flash(message=MESSAGES["hours"]["hours_added"], category="info")
        return render_template("control/hours/add_hours.html")
    return render_template("control/hours/add_hours.html")


@hours_bp.route("/delete/<int:hours_id>", methods=["POST"])
@login_required
@permission_required(["advanced"])
def delete_hours(hours_id: int) -> Response:
    db_manager.hours.delete_hours(hours_id)
    return redirect(url_for("control.hours.hours_table"))


@hours_bp.route("", methods=["GET"])
@login_required
@permission_required(["advanced"])
def hours_table() -> str:
    hours_list: List[Tuple[str]] = db_manager.hours.get_hours_list()

    context: Dict[str, Union[int, List[Tuple[str]]]] = {
        "hours_list": hours_list,
    }
    return render_template("control/hours/hours_table.html", **context)
