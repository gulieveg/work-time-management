from typing import Dict, List, Tuple, Union

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import login_required
from werkzeug.wrappers import Response

from app.db import DatabaseManager
from app.utils import MESSAGES, permission_required

tasks_bp: Blueprint = Blueprint("tasks", __name__, url_prefix="/tasks")
db_manager: DatabaseManager = DatabaseManager()


@tasks_bp.route("/add", methods=["GET", "POST"])
@login_required
@permission_required(["advanced"])
def add_task() -> Union[str, Response]:
    if request.method == "POST":
        order_name: str = request.form.get("order_name")
        order_number: str = request.form.get("order_number")
        spent_hours: str = request.form.get("spent_hours")

        employee_name

        db_manager.tasks.add_task()
