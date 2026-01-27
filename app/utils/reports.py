from collections import defaultdict
from datetime import datetime
from decimal import Decimal
from io import BytesIO
from typing import Dict, List, NamedTuple, Union

import pandas
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
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


def write_data_to_worksheet(
    worksheet: Worksheet,
    grouped_data: GroupedData,
    headers: Headers,
) -> None:
    dataframe: pandas.DataFrame = pandas.DataFrame(data=grouped_data, columns=headers)

    for r in dataframe_to_rows(dataframe, index=False, header=True):
        worksheet.append(r)

    worksheet.auto_filter.ref = worksheet.dimensions

    for cell in worksheet[1]:
        cell.font = Font(bold=True)

    for col_index, col in enumerate(worksheet.columns):
        width: int = len(str(worksheet[1][col_index].value))
        column: str = col[0].column_letter
        for cell in col:
            if len(str(cell.value)) > width:
                width: int = len(str(cell.value))
        adjusted_width: int = width + 10
        worksheet.column_dimensions[column].width = adjusted_width

    for row in worksheet.iter_rows():
        for cell in row:
            cell.alignment = Alignment(horizontal="center", vertical="center")


def write_data_to_task_worksheet(workbook: Workbook, tasks: Tasks) -> None:
    worksheet: Worksheet = workbook.active
    worksheet.title = "Все задания"

    headers: Headers = [
        "ФИО сотрудника",
        "Таб. номер",
        "Роль сотрудника",
        "Наименование подразделения",
        "Дата",
        "Номер заказа",
        "Наименование заказа",
        "Часы",
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
    worksheet.title = "Загруженность сотрудников"

    headers: Headers = [
        "ФИО сотрудника",
        "Таб. номер",
        "Роль сотрудника",
        "Наименование подразделения",
        "Дата",
        "Часы",
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

    grouped_data: GroupedData = [
        [
            key.employee_name,
            key.personnel_number,
            key.employee_category,
            key.department,
            datetime.strptime(key.operation_date, "%Y-%m-%d").date(),
            total_hours,
        ]
        for key, total_hours in aggregated_hours.items()
    ]

    write_data_to_worksheet(worksheet, grouped_data, headers)


def write_data_to_order_worksheet(workbook: Workbook, tasks: Tasks) -> None:
    worksheet: Worksheet = workbook.create_sheet()
    worksheet.title = "Данные по заказам"

    headers: Headers = [
        "Номер заказа",
        "Наименование заказа",
        "Часы",
    ]

    aggregated_hours: Dict[OrderKey, Decimal] = defaultdict(Decimal)

    for task in tasks:
        key: OrderKey = OrderKey(
            order_number=task["order_number"],
            order_name=task["order_name"],
        )
        aggregated_hours[key] += task["hours"]

    grouped_data: GroupedData = [
        [
            key.order_number,
            key.order_name,
            total_hours,
        ]
        for key, total_hours in aggregated_hours.items()
    ]

    write_data_to_worksheet(worksheet, grouped_data, headers)


def generate_report(tasks: Tasks) -> BytesIO:
    workbook: Workbook = Workbook()

    write_data_to_task_worksheet(workbook, tasks)
    write_data_to_employee_worksheet(workbook, tasks)
    write_data_to_order_worksheet(workbook, tasks)

    file: BytesIO = BytesIO()
    workbook.save(file)
    file.seek(0)
    return file
