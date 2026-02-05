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
        "work_name": request.args.get("work_name"),
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
    if request.method == "POST":
        employee_data: str = request.form.get("employee_data")
        operation_date: str = request.form.get("operation_date")
        order_names: List[str] = request.form.getlist("order_name[]")
        order_numbers: List[str] = request.form.getlist("order_number[]")

        if not operation_date:
            operation_date: str = datetime.now().strftime("%Y-%m-%d")

        employee_details: Tuple[str, str] = db_manager.employees.get_employee_details(employee_data)
        employee_name, personnel_number = employee_details

        employee_department: str = db_manager.employees.get_employee_department(personnel_number)
        employee_category: str = db_manager.employees.get_employee_category(personnel_number)

        for order_name, order_number in zip(order_names, order_numbers):
            work_entries: Dict[str, str] = {
                key.split("][")[1].rstrip("]"): value
                for key, value in request.form.items()
                if key.startswith(f"work_hours[{order_numbers[0]}]")
            }

            total_hours: Decimal = Decimal(0)
            for hours in work_entries.values():
                if hours:
                    if Decimal(hours) < Decimal(0):
                        flash(message=MESSAGES["tasks"]["hours_less_than_zero"], category="error")
                        return render_template("tasks/add_task.html")
                    total_hours += Decimal(hours)

            if total_hours > Decimal(8.25):
                flash(message=MESSAGES["tasks"]["hours_exceed_limit"], category="error")
                return render_template("tasks/add_task.html")

            for work_name, hours in work_entries.items():
                if hours and Decimal(hours):
                    args: Dict[str, Union[str, Decimal]] = {
                        "employee_name": employee_name,
                        "personnel_number": personnel_number,
                        "department": employee_department,
                        "work_name": work_name,
                        "hours": Decimal(hours),
                        "order_number": order_number,
                        "order_name": order_name,
                        "operation_date": operation_date,
                        "employee_category": employee_category,
                    }
        flash(message="Задания успешно добавлены.", category="info")
        return redirect(url_for("tasks.add_task"))
    return render_template("tasks/add_task.html")


@tasks_bp.route("/edit/<int:task_id>", methods=["GET", "POST"])
@login_required
@permission_required(["advanced", "standard"])
def edit_task(task_id: int) -> Union[str, Response]:
    task_data: Dict[str, Union[str, Decimal]] = db_manager.tasks.get_task_data_by_id(task_id)

    context: Dict[str, Union[str, Decimal]] = {
        "employee_name": task_data["employee_name"],
        "personnel_number": task_data["personnel_number"],
        "operation_date": task_data["operation_date"],
        "hours": task_data["hours"],
        "order_name": task_data["order_name"],
        "order_number": task_data["order_number"],
        "work_name": task_data["work_name"],
    }

    if request.method == "POST":
        employee_data: str = request.form.get("employee_data")
        operation_date: str = request.form.get("operation_date")
        hours: str = request.form.get("hours")
        order_name: str = request.form.get("order_name")
        order_number: str = request.form.get("order_number")
        work_name: str = request.form.get("work_name")

        employee_details: Tuple[str, str] = db_manager.employees.get_employee_details(employee_data)

        if employee_details is None:
            flash(message=MESSAGES["employees"]["invalid_employee_format"], category="warning")
            context: Dict[str, str] = {
                "operation_date": operation_date,
                "hours": hours,
                "order_name": order_name,
                "order_number": order_number,
                "work_name": work_name,
            }
            return render_template("tasks/edit_task.html", **context)

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
                "work_name": work_name,
            }
            return render_template("tasks/edit_task.html", **context)

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
                "work_name": work_name,
            }
            return render_template("tasks/edit_task.html", **context)

        args: Dict[str, Union[str, Decimal]] = {
            "task_id": task_id,
            "employee_name": employee_name,
            "personnel_number": personnel_number,
            "hours": Decimal(hours),
            "order_name": order_name,
            "order_number": order_number,
            "operation_date": operation_date,
            "work_name": work_name,
        }
        db_manager.tasks.update_task(**args)

        params: Dict[str, str] = {
            "departments[]": request.args.getlist("departments[]"),
            "start_date": request.args.get("start_date"),
            "end_date": request.args.get("end_date"),
            "employee_data": request.args.get("employee_data"),
            "order_number": request.args.get("order_number"),
            "work_name": request.args.get("work_name"),
            "order_name": request.args.get("order_name"),
        }
        return redirect(url_for("tasks.tasks_table", **params))
    return render_template("tasks/edit_task.html", **context)


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
        "work_name": request.form.get("work_name"),
        "order_name": request.form.get("order_name"),
    }
    db_manager.tasks.delete_task(task_id)
    return redirect(url_for("tasks.tasks_table", **params))

    # if not hours_list:
    #     flash(message=MESSAGES["tasks"]["no_tasks_provided"], category="warning")
    #     return redirect(url_for("tasks.add_task"))

    # if not operation_date:
    #     operation_date: str = datetime.now().strftime("%Y-%m-%d")

    # employee_details: Tuple[str, str] = db_manager.employees.get_employee_details(employee_data)

    # if employee_details is None:
    #     flash(message=MESSAGES["employees"]["invalid_employee_format"], category="warning")
    #     context: Dict[str, Union[str, List[str]]] = {
    #         "operation_date": operation_date,
    #         "hours_list": hours_list,
    #         "order_names": order_names,
    #         "order_numbers": order_numbers,
    #         "work_names": work_names,
    #     }
    #     return render_template("tasks/add_task.html", **context)

    # employee_name, personnel_number = employee_details

    # if not db_manager.employees.employee_exists(personnel_number):
    #     flash(message=MESSAGES["employees"]["employee_not_found"], category="warning")
    #     context: Dict[str, Union[str, List[str]]] = {
    #         "employee_data": employee_data,
    #         "operation_date": operation_date,
    #         "hours_list": hours_list,
    #         "order_names": order_names,
    #         "order_numbers": order_numbers,
    #         "work_names": work_names,
    #     }
    #     return render_template("tasks/add_task.html", **context)

    # free_hours: Decimal = db_manager.employees.get_employee_free_hours(personnel_number, operation_date)

    # if Decimal(sum(map(Decimal, hours_list))) > free_hours:
    #     message: str = MESSAGES["employees"]["exceeded_hours"].format(employee_data, free_hours)
    #     flash(message=message, category="warning")
    #     context: Dict[str, Union[str, List[str]]] = {
    #         "employee_data": employee_data,
    #         "operation_date": operation_date,
    #         "hours_list": hours_list,
    #         "order_names": order_names,
    #         "order_numbers": order_numbers,
    #         "work_names": work_names,
    #     }
    #     return render_template("tasks/add_task.html", **context)

    # employee_department: str = db_manager.employees.get_employee_department(personnel_number)
    # employee_category: str = db_manager.employees.get_employee_category(personnel_number)

    # for hours, order_number, order_name, work_name in zip(hours_list, order_numbers, order_names, work_names):
    #     args: Dict[str, Union[str, Decimal]] = {
    #         "employee_name": employee_name,
    #         "personnel_number": personnel_number,
    #         "department": employee_department,
    #         "employee_category": employee_category,
    #         "work_name": work_name,
    #         "hours": Decimal(hours),
    #         "order_number": order_number,
    #         "order_name": order_name,
    #         "operation_date": operation_date,
    #     }
    #     db_manager.tasks.add_task(**args)

    # flash(message=MESSAGES["tasks"]["tasks_added"], category="info")
    # return redirect(url_for("tasks.add_task"))
    # return render_template("tasks/add_task.html")
