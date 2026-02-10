from decimal import Decimal
from io import BytesIO
from typing import Dict, List, Union

import pandas
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, NamedStyle, Side
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.worksheet.worksheet import Worksheet

Tasks = List[Dict[str, Union[str, Decimal]]]
GroupedData = List[List[Union[str, Decimal]]]

Headers = List[str]


def write_orders_data(workbook: Workbook, grouped_data: GroupedData) -> None:
    headers: Headers = [
        "Номер заказа",
        "Наименование заказа",
        "Плановая трудоемкость, ч",
        "Фактическая трудоемкость, ч",
        "Остаточная трудоемкость, ч",
    ]

    dataframe: pandas.DataFrame = pandas.DataFrame(data=grouped_data, columns=headers)

    worksheet: Worksheet = workbook.active

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

    cell_style: NamedStyle = NamedStyle(name="cell_style", number_format="0.00")

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


def generate_report(grouped_data: GroupedData) -> BytesIO:
    workbook: Workbook = Workbook()

    write_orders_data(workbook, grouped_data)

    file: BytesIO = BytesIO()
    workbook.save(file)
    file.seek(0)
    return file
