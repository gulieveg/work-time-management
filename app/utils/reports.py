from decimal import Decimal
from io import BytesIO
from typing import Dict, List, Union

import pandas
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, NamedStyle, Side
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.worksheet.worksheet import Worksheet

Data = List[List[Union[str, Decimal]]]


def write_tasks_data(workbook: Workbook, tasks_data: Data) -> None:
    headers: List[str] = [
        "ФИО сотрудника",
        "Таб. номер",
        "Категория сотрудника",
        "Наименование подразделения",
        "Номер заказа",
        "Наименование заказа",
        "Наименование работы",
        "Затраченное время, ч",
        "Дата выполнения",
    ]

    dataframe: pandas.DataFrame = pandas.DataFrame(data=tasks_data, columns=headers)

    worksheet: Worksheet = workbook.active
    worksheet.title = "Sheet 1"

    for row in dataframe_to_rows(dataframe, index=False, header=True):
        worksheet.append(row)

    worksheet.auto_filter.ref = worksheet.dimensions

    for cell in worksheet[1]:
        cell.font = Font(bold=True)

    column_widths: Dict[str, int] = {
        "A": 28,
        "B": 18,
        "C": 18,
        "D": 22,
        "E": 22,
        "F": 44,
        "G": 44,
        "H": 18,
        "I": 24,
    }

    cell_style: NamedStyle = NamedStyle(name="cell_style-1", number_format="0.00")

    for col in worksheet.columns:
        column_letter: str = col[0].column_letter

        worksheet.column_dimensions[column_letter].width = column_widths[column_letter]

        for cell in col:
            if cell.row > 1 and column_letter == "H":
                cell.style = cell_style
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    border_style = Border(
        Side(border_style="thin"),
        Side(border_style="thin"),
        Side(border_style="thin"),
        Side(border_style="thin"),
    )

    for row in worksheet.iter_rows():
        for cell in row:
            cell.border = border_style


def write_employees_data(workbook: Workbook, employees_data: Data) -> None:
    headers: List[str] = [
        "ФИО сотрудника",
        "Таб. номер",
        "Категория сотрудника",
        "Наименование подразделения",
        "Затраченное время, ч",
        "Дата выполнения",
    ]

    dataframe: pandas.DataFrame = pandas.DataFrame(data=employees_data, columns=headers)

    worksheet: Worksheet = workbook.create_sheet()
    worksheet.title = "Sheet 2"

    for row in dataframe_to_rows(dataframe, index=False, header=True):
        worksheet.append(row)

    worksheet.auto_filter.ref = worksheet.dimensions

    for cell in worksheet[1]:
        cell.font = Font(bold=True)

    column_widths: Dict[str, int] = {
        "A": 28,
        "B": 18,
        "C": 18,
        "D": 22,
        "E": 18,
        "F": 24,
    }

    cell_style: NamedStyle = NamedStyle(name="cell_style-2", number_format="0.00")

    for col in worksheet.columns:
        column_letter: str = col[0].column_letter

        worksheet.column_dimensions[column_letter].width = column_widths[column_letter]

        for cell in col:
            if cell.row > 1 and column_letter == "F":
                cell.style = cell_style
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    border_style = Border(
        Side(border_style="thin"),
        Side(border_style="thin"),
        Side(border_style="thin"),
        Side(border_style="thin"),
    )

    for row in worksheet.iter_rows():
        for cell in row:
            cell.border = border_style


def write_orders_data(workbook: Workbook, orders_data: Data) -> None:
    headers: List[str] = [
        "Номер заказа",
        "Наименование заказа",
        "Плановая трудоемкость, ч",
        "Фактическая трудоемкость, ч",
        "Остаточная трудоемкость, ч",
    ]

    dataframe: pandas.DataFrame = pandas.DataFrame(data=orders_data, columns=headers)

    worksheet: Worksheet = workbook.create_sheet()
    worksheet.title = "Sheet 3"

    for row in dataframe_to_rows(dataframe, index=False, header=True):
        worksheet.append(row)

    worksheet.auto_filter.ref = "A1:B1"

    for cell in worksheet[1]:
        cell.font = Font(bold=True)

    column_widths: Dict[str, int] = {
        "A": 22,
        "B": 66,
        "C": 22,
        "D": 22,
        "E": 22,
    }

    cell_style: NamedStyle = NamedStyle(name="cell_style-3", number_format="0.00")

    for col in worksheet.columns:
        column_letter: str = col[0].column_letter

        worksheet.column_dimensions[column_letter].width = column_widths[column_letter]

        for cell in col:
            if cell.row > 1 and column_letter in ["C", "D", "E"]:
                cell.style = cell_style
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    last_row: int = worksheet.max_row

    worksheet.merge_cells(f"A{last_row}:B{last_row}")

    for cell in worksheet[last_row]:
        cell.font = Font(bold=True)

    border_style = Border(
        Side(border_style="thin"),
        Side(border_style="thin"),
        Side(border_style="thin"),
        Side(border_style="thin"),
    )

    for row in worksheet.iter_rows():
        for cell in row:
            cell.border = border_style


def generate_report(tasks_data: Data, employees_data: Data, orders_data: Data) -> BytesIO:
    workbook: Workbook = Workbook()

    write_tasks_data(workbook, tasks_data)
    write_employees_data(workbook, employees_data)
    write_orders_data(workbook, orders_data)

    file: BytesIO = BytesIO()
    workbook.save(file)
    file.seek(0)
    return file
