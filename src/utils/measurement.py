import locale
import os
import xml.etree.ElementTree as ET

import pandas as pd

from config.database import Mdb

locale.setlocale(
    locale.LC_TIME, "Portuguese_Brazil.1252"
)  # Necessário para colocar a data

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
                    "diameter_land": shots_list.get("diameter-land"),
                    "diameter_groove": shots_list.get("diameter-groove"),
                    # "status": shots_list.get("status"),
                    # "depth": shots_list.get("depth"),
                    # "groove_is_ready": shots_list.get("groove-is-ready"),
                    # "index": shots_list.get("index"),
                    # "land_is_ready": shots_list.get("land-is-ready"),
                    # "is_depth_measured": shots_list.get("is-depth-measured"),
                    # "is_valid": shots_list.get("is-valid")
                }
                data.append(entry)
        except ET.ParseError as e:
            print(f"Error parsing file {location}: {e}")
    return pd.DataFrame(data)


def raw_extracted_data():
    with Mdb() as db:
        dataframe = db.fetch("measurements")

    rough_data = get_rough_data(dataframe["data_file"])
    dataframe = dataframe.merge(
        rough_data, how="inner", on=["data_file", "position_id"]
    )

    return dataframe


def transform_columns(df: pd.DataFrame):
    df["diameter_land"] = df["diameter_land"].astype(float)
    df["diameter_groove"] = df["diameter_groove"].astype(float)
    df["measurement_date"] = df["measurement_date"].dt.date

    return df


def extract_measurement_data(archives: list = []):
    dataframe = raw_extracted_data()

    if archives:
        dataframe = dataframe[dataframe["archive_name"].isin(archives)]

    dataframe = transform_columns(dataframe)
    columns = [
        "measurement_date",
        "measurement_name",
        "depth",
        "diameter_land",
        "diameter_groove",
    ]

    if dataframe["diameter_groove"].max() == 0:
        columns.remove("diameter_groove")

    dataframe = dataframe[columns]

    return dataframe
