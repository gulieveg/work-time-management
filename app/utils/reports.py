from decimal import Decimal
from io import BytesIO
from typing import Dict, List, Union

import pandas
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, NamedStyle, Side
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.worksheet.worksheet import Worksheet

Data = List[List[Union[str, Decimal]]]


def set_column_styles(worksheet: Worksheet, columns: Dict[str, int], style_columns: List[str]) -> None:
    cell_style: NamedStyle = NamedStyle(name="cell-style", number_format="0.00")
    border_style = Border(
        Side(border_style="thin"),
        Side(border_style="thin"),
        Side(border_style="thin"),
        Side(border_style="thin"),
    )

    for column in worksheet.columns:
        column_letter: str = column[0].column_letter
        worksheet.column_dimensions[column_letter].width = columns[column_letter]

        for cell in column:
            if cell.row > 1 and column_letter in style_columns:
                cell.style = cell_style
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            cell.border = border_style


def write_data(
    workbook: Workbook,
    sheet_name: str,
    headers: List[str],
    data: Data,
    column_widths: Dict[str, int],
    style_columns: List[str],
) -> None:
    dataframe = pandas.DataFrame(data=data, columns=headers)
    worksheet = workbook.create_sheet(sheet_name)

    for row in dataframe_to_rows(dataframe, index=False, header=True):
        worksheet.append(row)

    worksheet.auto_filter.ref = worksheet.dimensions
    for cell in worksheet[1]:
        cell.font = Font(bold=True)

    set_column_styles(worksheet, column_widths, style_columns)


# Основная функция для генерации отчета
def generate_report(tasks_data: Data, employees_data: Data, orders_data: Data) -> BytesIO:
    workbook = Workbook()

    workbook.remove(workbook.active)

    # Настройка данных для каждой таблицы
    write_data(
        workbook,
        "Tasks",
        [
            "ФИО сотрудника",
            "Таб. номер",
            "Категория сотрудника",
            "Наименование подразделения",
            "Номер заказа",
            "Наименование заказа",
            "Наименование работы",
            "Затраченное время, ч",
            "Дата выполнения",
        ],
        tasks_data,
        {"A": 28, "B": 18, "C": 18, "D": 22, "E": 22, "F": 44, "G": 44, "H": 18, "I": 24},
        style_columns=["H"],
    )

    write_data(
        workbook,
        "Employees",
        [
            "ФИО сотрудника",
            "Таб. номер",
            "Категория сотрудника",
            "Наименование подразделения",
            "Дата выполнения",
            "Затраченное время, ч",
        ],
        employees_data,
        {"A": 28, "B": 18, "C": 18, "D": 22, "E": 24, "F": 18},
        style_columns=["F"],
    )

    write_data(
        workbook,
        "Orders",
        [
            "Номер заказа",
            "Наименование заказа",
            "Плановая трудоемкость, ч",
            "Фактическая трудоемкость, ч",
            "Остаточная трудоемкость, ч",
        ],
        orders_data,
        {"A": 22, "B": 66, "C": 22, "D": 22, "E": 22},
        style_columns=["C", "D", "E"],
    )

    # Добавляем жирный шрифт для последней строки в таблице "Orders"
    worksheet = workbook["Orders"]
    last_row = worksheet.max_row
    worksheet.merge_cells(f"A{last_row}:B{last_row}")
    for cell in worksheet[last_row]:
        cell.font = Font(bold=True)

    # Сохраняем в файл
    file = BytesIO()
    workbook.save(file)
    file.seek(0)
    return file
