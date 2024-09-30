from datetime import datetime

import openpyxl
import pandas as pd

from utils import open_excel_file
from utils.measurement import extract_measurement_data

TEMPLATE_FILE = r"C:/Users/HPI/Documents/BGS/src/template.xlsx"
OUTPUT_FOLDER = r"C:/Users/HPI/Documents/Relatórios Gerados/"


def rename_columns(dataframe: pd.DataFrame):
    return dataframe.rename(
        {
            "system_name": "Sistema Utilizado",
            "measurement_name": "Nome do Ensaio",
            "archive_name": "Nome do Arquivo",
            "measurement_date": "Data do Ensaio",
            "depth": "Profundidade (mm)",
            "diameter_land": "Diâmetro Cheio (mm)",
            "diameter_groove": "Diâmetro Fundo (mm)",
        },
        axis=1,
    )


def generate_report(
    report_data: dict, archives: list = [], template_file: str = TEMPLATE_FILE
):
    dataframe = extract_measurement_data(archives)

    wb = openpyxl.load_workbook(template_file)
    ws = wb.create_sheet(title="dados")

    today = datetime.now()  # .strftime("%Y-%m-%d")

    date_values_for_report = {
        "date": today.strftime("%d/%m/%Y"),
        "year": str(today.year),
        "extended_date": today.strftime("%d de %B de %Y"),
        "measurement_date": dataframe["measurement_date"]
        .unique()
        .min()
        .strftime("%d/%m/%Y"),
    }

    report_data = report_data | date_values_for_report

    for row in wb.worksheets[0]:  # first page
        for cell in row:
            if isinstance(cell.value, str) and (
                "<" in cell.value and ">" in cell.value
            ):
                for key, value in report_data.items():
                    cell.value = cell.value.replace(f"<{key}>", value)

    filename = f"{OUTPUT_FOLDER}/{", ".join(archives)}.xlsx"

    wb.save(filename)
    write_dataframe(filename, wb, dataframe)
    open_excel_file(filename)


def write_dataframe(
    filename: str, workbook: openpyxl.Workbook, dataframe: pd.DataFrame
):
    dataframe = rename_columns(dataframe).reset_index()

    if "Diâmetro Fundo (mm)" in dataframe.columns:
        pivot_df = pd.pivot_table(
            data=dataframe,
            index="Profundidade (mm)",
            columns="Nome do Ensaio",
            values=["Diâmetro Cheio (mm)", "Diâmetro Fundo (mm)"],
        ).T
    else:
        pivot_df = pd.pivot_table(
            data=dataframe,
            index="Nome do Ensaio",
            columns="Profundidade (mm)",
            values="Diâmetro Cheio (mm)",
        )

    with pd.ExcelWriter(
        filename, engine="openpyxl", mode="a", if_sheet_exists="replace"
    ) as writer:
        pivot_df.to_excel(writer, sheet_name="dados")
