from decimal import Decimal
from typing import Dict, List, Tuple, Union

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import login_required
from werkzeug.wrappers import Response

from app.db import DatabaseManager
from app.utils import MESSAGES, permission_required

Tasks = List[Dict[str, Union[str, Decimal]]]

orders_bp: Blueprint = Blueprint("orders", __name__, url_prefix="/orders")
db_manager: DatabaseManager = DatabaseManager()


@orders_bp.route("/", methods=["GET"])
@login_required
@permission_required(["advanced"])
def orders_table() -> str:
    order_number: str = request.args.get("order_number")
    order_name: str = request.args.get("order_name")

    args: Dict[str, str] = {
        "order_number": order_number,
        "order_name": order_name,
    }

    filtered_orders: List[Tuple[str]] = db_manager.orders.get_orders(**args)
    if not filtered_orders:
        return render_template("control/orders/orders_table.html")

    page: int = request.args.get("page", 1, int)

    args: Dict[str, Union[str, int]] = {
        "order_number": order_number,
        "order_name": order_name,
        "page": page,
    }

    filtered_orders_page: List[Tuple[str]] = db_manager.orders.get_orders(**args)

    context: Dict[str, Union[int, List[Tuple[str]]]] = {
        "filtered_orders": filtered_orders,
        "filtered_orders_page": filtered_orders_page,
        "page": page,
    }
    return render_template("control/orders/orders_table.html", **context)


@orders_bp.route("/add", methods=["GET", "POST"])
@login_required
@permission_required(["advanced"])
def add_order() -> str:
    if request.method == "POST":
        order_number: str = request.form.get("order_number")
        order_name: str = request.form.get("order_name")
        db_manager.orders.add_order(order_number, order_name)
        flash(message=MESSAGES["orders"]["order_added"], category="info")
        return render_template("control/orders/add_order.html")
    return render_template("control/orders/add_order.html")


@orders_bp.route("/edit/<int:order_id>", methods=["GET", "POST"])
@login_required
@permission_required(["advanced"])
def edit_order(order_id: int) -> Union[str, Response]:
    order: Tuple[str] = db_manager.orders.get_order_by_id(order_id)

    context: Dict[str, str] = {
        "order_number": order["order_number"],
        "order_name": order["order_name"],
    }

    if request.method == "POST":
        order_number: str = request.form["order_number"]
        order_name: str = request.form["order_name"]

        args: Dict[str, Union[str, int]] = {
            "order_id": order_id,
            "order_number": order_number,
            "order_name": order_name,
        }
        db_manager.orders.update_order(**args)
        flash(message=MESSAGES["orders"]["order_updated"], category="info")
        return redirect(url_for("control.orders.edit_order", order_id=order_id))
    return render_template("control/orders/edit_order.html", **context)


@orders_bp.route("/delete/<int:order_id>", methods=["POST"])
@login_required
@permission_required(["advanced"])
def delete_order(order_id: int) -> Response:
    page: int = request.form.get("page", 1, int)
    db_manager.orders.delete_order(order_id)
    return redirect(url_for("control.orders.orders_table", page=page))


@orders_bp.route("/names", methods=["GET"])
@login_required
def get_order_names() -> Response:
    query: str = request.args.get("query", "")
    order_names: List[str] = db_manager.orders.get_order_names_by_partial_match(query)
    return jsonify(order_names)


@orders_bp.route("/numbers", methods=["GET"])
@login_required
def get_order_numbers() -> Response:
    query: str = request.args.get("query", "")
    order_numbers: List[str] = db_manager.orders.get_order_numbers_by_partial_match(query)
    return jsonify(order_numbers)


@orders_bp.route("/<string:order_number>/name", methods=["GET"])
@login_required
def get_order_name(order_number: str) -> Response:
    order_name: str = db_manager.orders.get_order_name_by_number(order_number)
    return jsonify({"order_name": order_name})


@orders_bp.route("/<string:order_name>/number", methods=["GET"])
@login_required
def get_order_number(order_name: str) -> Response:
    order_number: str = db_manager.orders.get_order_number_by_name(order_name)
    return jsonify({"order_number": order_number})
