from decimal import Decimal
from typing import Dict, List, Tuple, Union

from flask import Blueprint, Response, flash, redirect, render_template, request, url_for
from flask_login import login_required

from app.db import DatabaseManager
from app.utils import MESSAGES, permission_required

hours_bp: Blueprint = Blueprint("hours", __name__, url_prefix="/hours")
db_manager: DatabaseManager = DatabaseManager()


@hours_bp.route("/add-spent-hours", methods=["GET", "POST"])
@login_required
@permission_required(["advanced"])
def add_hours() -> Union[str, Response]:
    return render_template("control/hours/add_hours.html")
