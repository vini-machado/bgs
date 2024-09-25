from datetime import datetime
import os
import pandas as pd 
import openpyxl
import xml.etree.ElementTree as ET
from config.database import Mdb
from pathlib import Path
import locale
from utils import open_excel_file

locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil.1252') # Necessário para colocar a data

ROUGH_DATA_FOLDER = r"C:/HPI_BWF/rough_data/"

def get_rough_data(rough_data_locations: pd.Series):
    locations = rough_data_locations.unique()
    data = []

    for location in locations:
        file_path = os.path.join(ROUGH_DATA_FOLDER, location)
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            # Find all <shots-list> tags
            for shots_list in root.findall(".//shots-list"):
                # Extract attributes from <shots-list>
                entry = {
                    "data_file": location,
                    "position_id": int(shots_list.get("position-iD", 0)),
                    "measurement": shots_list.get("diameter-land"),
                    # "status": shots_list.get("status"),
                    # "depth": shots_list.get("depth"),
                    # "groove_is_ready": shots_list.get("groove-is-ready"),
                    # "index": shots_list.get("index"),
                    # "diameter_groove": shots_list.get("diameter-groove"),
                    # "land_is_ready": shots_list.get("land-is-ready"),
                    # "is_depth_measured": shots_list.get("is-depth-measured"),
                    # "is_valid": shots_list.get("is-valid")
                }
                data.append(entry)
        except ET.ParseError as e:
            print(f"Error parsing file {location}: {e}")
    return pd.DataFrame(data)

def get_measurements(archives: list = [], report_data: dict = {}, should_open_file: bool = True):
    with Mdb() as db:
        dataframe = db.fetch('measurements')

    rough_data = get_rough_data(dataframe['data_file'])
    dataframe = dataframe.merge(rough_data, how='inner', on=['data_file', 'position_id'])

    dataframe = dataframe[['system_name', 'measurement_name', 'archive_name', 'measurement_date', 'depth', 'measurement']]
    dataframe['measurement'] = dataframe['measurement'].astype(float) 
    
    if archives:
        dataframe = dataframe[dataframe['archive_name'].isin(archives)]

    save_path = export_measurements(dataframe)
    write_report(report_data)

    if should_open_file:
        open_excel_file(save_path)

    return dataframe

def export_measurements(dataframe: pd.DataFrame) -> Path:
    today = datetime.now().strftime("%Y-%m-%d")

    save_path = Path(os.getcwd()).parent.joinpath('exports', f'{today}.xlsx')
    dataframe.to_excel(save_path, index=False)

    return save_path

def write_report(report_data: dict, template_file: str = r"C:/Users/HPI/Documents/BGS/src/template.xlsx"):
    wb = openpyxl.load_workbook(template_file)
    today = datetime.now() #.strftime("%Y-%m-%d")

    date_values_for_report = {
        'date': today.strftime("%d/%m/%Y"),
        'year': str(today.year),
        'extended_date': today.strftime("%d de %B de %Y")
    }

    report_data = report_data | date_values_for_report

    for row in wb.worksheets[0]: # first page
        for cell in row:
            if isinstance(cell.value, str) and ('<' in cell.value and '>' in cell.value):
                for key, value in report_data.items():
                    cell.value = cell.value.replace(f"<{key}>", value)


    wb.save("C:/Users/HPI/Documents/BGS/src/template_escrito.xlsx")
    open_excel_file("C:/Users/HPI/Documents/BGS/src/template_escrito.xlsx")

