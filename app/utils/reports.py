from collections import defaultdict
from datetime import datetime
from decimal import Decimal
from io import BytesIO
from typing import Dict, List, NamedTuple, Union

import pandas
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, NamedStyle, Side
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.worksheet.worksheet import Worksheet

Tasks = List[Dict[str, Union[str, Decimal]]]
GroupedData = List[List[Union[str, Decimal]]]
Headers = List[str]


class EmployeeKey(NamedTuple):
    employee_name: str
    personnel_number: str
    employee_category: str
    department: str
    operation_date: str


class OrderKey(NamedTuple):
    order_number: str
    order_name: str


def write_data_to_worksheet(worksheet: Worksheet, grouped_data: GroupedData, headers: Headers) -> None:
    dataframe: pandas.DataFrame = pandas.DataFrame(data=grouped_data, columns=headers)

    for r in dataframe_to_rows(dataframe, index=False, header=True):
        worksheet.append(r)

    worksheet.auto_filter.ref = "A1:B1"

    for cell in worksheet[1]:
        cell.font = Font(bold=True)

    column_widths: Dict[str, int] = {
        "A": 22,
        "B": 44,
        "C": 22,
        "D": 22,
        "E": 22,
    }

    number_style = NamedStyle(name="number_style", number_format="0.00")

    for col in worksheet.columns:
        column_letter = col[0].column_letter

        worksheet.column_dimensions[column_letter].width = column_widths[column_letter]

        for cell in col:
            if cell.row > 1 and column_letter in ["C", "D", "E"]:
                cell.style = number_style
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    border_style = Border(
        Side(border_style="thin"),
        Side(border_style="thin"),
        Side(border_style="thin"),
        Side(border_style="thin"),
    )

    last_row = worksheet.max_row

    worksheet.merge_cells(f"A{last_row}:B{last_row}")

    for row in worksheet.iter_rows():
        for cell in row:
            cell.border = border_style


def write_data_to_order_worksheet(workbook: Workbook, grouped_data: GroupedData) -> None:
    worksheet: Worksheet = workbook.active
    # worksheet.title = "Заказы"

    headers: Headers = [
        "Номер заказа",
        "Наименование заказа",
        "Плановая трудоемкость, ч",
        "Фактическая трудоемкость, ч",
        "Остаточная трудоемкость, ч",
    ]

    write_data_to_worksheet(worksheet, grouped_data, headers)


def generate_report(grouped_data: GroupedData) -> BytesIO:
    workbook: Workbook = Workbook()

    # write_data_to_task_worksheet(workbook, grouped_data)
    # write_data_to_employee_worksheet(workbook, grouped_data)

    write_data_to_order_worksheet(workbook, grouped_data)

    file: BytesIO = BytesIO()
    workbook.save(file)
    file.seek(0)
    return file


def write_data_to_task_worksheet(workbook: Workbook, tasks: Tasks) -> None:
    worksheet: Worksheet = workbook.active
    worksheet.title = "Задания"

    headers: Headers = [
        "ФИО сотрудника",
        "Таб. номер",
        "Роль сотрудника",
        "Наименование подразделения",
        "Дата",
        "Номер заказа",
        "Наименование заказа",
        "Фактическая трудоемкость, ч",
    ]

    categories: Dict[str, str] = {
        "worker": "Рабочий",
        "specialist": "Специалист",
        "manager": "Ведущий специалист",
    }

    grouped_data: GroupedData = [
        [
            task["employee_name"],
            task["personnel_number"],
            categories[task["employee_category"]],
            task["department"],
            datetime.strptime(task["operation_date"], "%Y-%m-%d").date(),
            task["order_number"],
            task["order_name"],
            task["hours"],
        ]
        for task in tasks
    ]

    write_data_to_worksheet(worksheet, grouped_data, headers)


def write_data_to_employee_worksheet(workbook: Workbook, tasks: Tasks) -> None:
    worksheet: Worksheet = workbook.create_sheet()
    worksheet.title = "Сотрудники"

    headers: Headers = [
        "ФИО сотрудника",
        "Таб. номер",
        "Роль сотрудника",
        "Наименование подразделения",
        "Дата",
        "Фактическая трудоемкость, ч",
    ]

    aggregated_hours: Dict[EmployeeKey, Decimal] = defaultdict(Decimal)

    for task in tasks:
        key: EmployeeKey = EmployeeKey(
            employee_name=task["employee_name"],
            personnel_number=task["personnel_number"],
            employee_category=task["employee_category"],
            department=task["department"],
            operation_date=task["operation_date"],
        )
        aggregated_hours[key] += task["hours"]

    categories: Dict[str, str] = {
        "worker": "Рабочий",
        "specialist": "Специалист",
        "manager": "Ведущий специалист",
    }

    grouped_data: GroupedData = [
        [
            key.employee_name,
            key.personnel_number,
            categories[key.employee_category],
            key.department,
            datetime.strptime(key.operation_date, "%Y-%m-%d").date(),
            spent_hours,
        ]
        for key, spent_hours in aggregated_hours.items()
    ]

    write_data_to_worksheet(worksheet, grouped_data, headers)
