from datetime import datetime
from decimal import Decimal
from io import BytesIO
from typing import Dict, List, Tuple, Union

from flask import Blueprint, flash, redirect, render_template, request, send_file, url_for
from flask_login import login_required
from werkzeug.wrappers import Response

from app.db import DatabaseManager
from app.utils import MESSAGES, generate_report, permission_required

Tasks = List[Dict[str, Union[str, Decimal]]]

tasks_bp: Blueprint = Blueprint("tasks", __name__, url_prefix="/tasks")
db_manager: DatabaseManager = DatabaseManager()


@tasks_bp.route("/table", methods=["GET"])
@login_required
def tasks_table() -> Union[str, Response]:
    args: Dict[str, str] = {
        "departments": request.args.getlist("departments[]"),
        "start_date": request.args.get("start_date"),
        "end_date": request.args.get("end_date"),
        "employee_data": request.args.get("employee_data"),
        "order_number": request.args.get("order_number"),
        "operation_type": request.args.get("operation_type"),
        "order_name": request.args.get("order_name"),
    }

    tasks: Tasks = db_manager.tasks.get_tasks(**args)
    departments: List[str] = db_manager.employees.get_departments()

    if request.args.get("export"):
        file: BytesIO = generate_report(tasks)
        return send_file(file, as_attachment=True, download_name="report.xlsx")

    today: str = datetime.today().strftime("%Y-%m-%d")
    context: Dict[str, Union[str, Tasks]] = {
        "tasks": tasks,
        "departments": departments,
        "today": today,
    }
    return render_template("tasks/tasks_table.html", **context)


@tasks_bp.route("/add", methods=["GET", "POST"])
@login_required
@permission_required(["advanced", "standard"])
def add_task() -> Union[str, Response]:
    work_types_data: List[str] = db_manager.employees.get_work_types()

    if request.method == "POST":
        employee_data: str = request.form.get("employee_data")
        operation_date: str = request.form.get("operation_date")
        hours_list: List[str] = request.form.getlist("hours[]")
        order_names: List[str] = request.form.getlist("order_name[]")
        order_numbers: List[str] = request.form.getlist("order_number[]")
        work_types: List[str] = request.form.getlist("work_type[]")

        if not hours_list:
            flash(message=MESSAGES["tasks"]["no_tasks_provided"], category="warning")
            return redirect(url_for("tasks.add_task"))

        if not operation_date:
            operation_date: str = datetime.now().strftime("%Y-%m-%d")

        employee_details: Tuple[str, str] = db_manager.employees.get_employee_details(employee_data)

        if employee_details is None:
            flash(message=MESSAGES["employees"]["invalid_employee_format"], category="warning")
            context: Dict[str, Union[str, List[str]]] = {
                "operation_date": operation_date,
                "hours_list": hours_list,
                "order_names": order_names,
                "order_numbers": order_numbers,
                "work_types": work_types,
            }
            return render_template("tasks/add_task.html", **context, work_types_data=work_types_data)

        employee_name, personnel_number = employee_details

        if not db_manager.employees.employee_exists(personnel_number):
            flash(message=MESSAGES["employees"]["employee_not_found"], category="warning")
            context: Dict[str, Union[str, List[str]]] = {
                "employee_data": employee_data,
                "operation_date": operation_date,
                "hours_list": hours_list,
                "order_names": order_names,
                "order_numbers": order_numbers,
                "work_types": work_types,
            }
            return render_template("tasks/add_task.html", **context, work_types_data=work_types_data)

        free_hours: Decimal = db_manager.employees.get_employee_free_hours(personnel_number, operation_date)

        if Decimal(sum(map(Decimal, hours_list))) > free_hours:
            message: str = MESSAGES["employees"]["exceeded_hours"].format(employee_data, free_hours)
            flash(message=message, category="warning")
            context: Dict[str, Union[str, List[str]]] = {
                "employee_data": employee_data,
                "operation_date": operation_date,
                "hours_list": hours_list,
                "order_names": order_names,
                "order_numbers": order_numbers,
                "work_types": work_types,
            }
            return render_template("tasks/add_task.html", **context, work_types_data=work_types_data)

        employee_department: str = db_manager.employees.get_employee_department(personnel_number)
        employee_category: str = db_manager.employees.get_employee_category(personnel_number)

        if work_types:
            operation_types: List[str] = work_types
        else:
            operation_type: str = db_manager.employees.get_employee_operation_type(personnel_number)
            operation_types: List[str] = [operation_type] * len(hours_list)

        for hours, order_number, order_name, operation_type in zip(
            hours_list, order_numbers, order_names, operation_types
        ):
            args: Dict[str, Union[str, Decimal]] = {
                "employee_name": employee_name,
                "personnel_number": personnel_number,
                "department": employee_department,
                "employee_category": employee_category,
                "operation_type": operation_type,
                "hours": Decimal(hours),
                "order_number": order_number,
                "order_name": order_name,
                "operation_date": operation_date,
            }
            db_manager.tasks.add_task(**args)

        flash(message=MESSAGES["tasks"]["tasks_added"], category="info")
        return redirect(url_for("tasks.add_task"))
    return render_template("tasks/add_task.html", work_types_data=work_types_data)


@tasks_bp.route("/edit/<int:task_id>", methods=["GET", "POST"])
@login_required
@permission_required(["advanced", "standard"])
def edit_task(task_id: int) -> Union[str, Response]:
    task: Dict[str, Union[str, Decimal]] = db_manager.tasks.get_task_by_id(task_id)

    context: Dict[str, Union[str, Decimal]] = {
        "employee_name": task["employee_name"],
        "personnel_number": task["personnel_number"],
        "operation_date": task["operation_date"],
        "hours": task["hours"],
        "order_name": task["order_name"],
        "order_number": task["order_number"],
        "work_type": task["operation_type"],
    }

    work_types_data: List[str] = db_manager.employees.get_work_types()

    if request.method == "POST":
        employee_data: str = request.form.get("employee_data")
        operation_date: str = request.form.get("operation_date")
        hours: str = request.form.get("hours")
        order_name: str = request.form.get("order_name")
        order_number: str = request.form.get("order_number")
        operation_type: str = request.form.get("work_type")

        employee_details: Tuple[str, str] = db_manager.employees.get_employee_details(employee_data)

        if employee_details is None:
            flash(message=MESSAGES["employees"]["invalid_employee_format"], category="warning")
            context: Dict[str, str] = {
                "operation_date": operation_date,
                "hours": hours,
                "order_name": order_name,
                "order_number": order_number,
                "work_type": operation_type,
            }
            return render_template("tasks/edit_task.html", **context, work_types_data=work_types_data)

        employee_name, personnel_number = employee_details

        if not db_manager.employees.employee_exists(personnel_number):
            flash(message=MESSAGES["employees"]["employee_not_found"], category="warning")
            context: Dict[str, str] = {
                "employee_name": employee_name,
                "personnel_number": personnel_number,
                "operation_date": operation_date,
                "hours": hours,
                "order_name": order_name,
                "order_number": order_number,
                "work_type": operation_type,
            }
            return render_template("tasks/edit_task.html", **context, work_types_data=work_types_data)

        free_hours: Decimal = db_manager.employees.get_employee_free_hours(personnel_number, operation_date)

        if Decimal(hours) > free_hours + context["hours"]:
            free_hours: Decimal = free_hours + context["hours"]
            message: str = MESSAGES["employees"]["exceeded_hours"].format(employee_data, free_hours)
            flash(message=message, category="warning")
            context: Dict[str, str] = {
                "employee_name": employee_name,
                "personnel_number": personnel_number,
                "operation_date": operation_date,
                "hours": hours,
                "order_name": order_name,
                "order_number": order_number,
                "work_type": operation_type,
            }
            return render_template("tasks/edit_task.html", **context, work_types_data=work_types_data)

        args: Dict[str, Union[str, Decimal]] = {
            "task_id": task_id,
            "employee_name": employee_name,
            "personnel_number": personnel_number,
            "hours": Decimal(hours),
            "order_name": order_name,
            "order_number": order_number,
            "operation_date": operation_date,
            "operation_type": operation_type,
        }
        db_manager.tasks.update_task(**args)

        params: Dict[str, str] = {
            "departments[]": request.args.getlist("departments[]"),
            "start_date": request.args.get("start_date"),
            "end_date": request.args.get("end_date"),
            "employee_data": request.args.get("employee_data"),
            "order_number": request.args.get("order_number"),
            "operation_type": request.args.get("operation_type"),
            "order_name": request.args.get("order_name"),
        }
        return redirect(url_for("tasks.tasks_table", **params))
    return render_template("tasks/edit_task.html", **context, work_types_data=work_types_data)


@tasks_bp.route("/delete/<int:task_id>", methods=["POST"])
@login_required
@permission_required(["advanced", "standard"])
def delete_task(task_id: str) -> Response:
    params: Dict[str, str] = {
        "departments[]": request.form.getlist("departments[]"),
        "start_date": request.form.get("start_date"),
        "end_date": request.form.get("end_date"),
        "employee_data": request.form.get("employee_data"),
        "order_number": request.form.get("order_number"),
        "operation_type": request.form.get("operation_type"),
        "order_name": request.form.get("order_name"),
    }
    db_manager.tasks.delete_task(task_id)
    return redirect(url_for("tasks.tasks_table", **params))
