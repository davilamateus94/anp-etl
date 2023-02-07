import glob
import wget
import os
import zipfile
from loguru import logger
import pandas as pd


def get_tables_to_download():

    return pd.read_json("anp_etl/catalog/tables.json", orient="index")


def download_raw_data(tables, i):

    timeout = 60
    file = tables.iloc[i]

    url = file["path"]
    logger.info(f"url:{url}")
    file_type = file["path"].split(".")[-1]
    logger.info(f"file_type:{file_type}")
    file_name = file["name"]
    logger.info(f"file_type:{file_name}")

    saved_files = [file.split("/")[-1] for file in glob.glob("data/bronze/*.csv")]

    if file_name in saved_files:

        logger.info(f"File already downloaded and saved in data/bronze/{file_name}")

        return f"data/bronze/{file_name}"

    logger.info(f"Downloading file: {file_name} - {file_type.upper()} type")

    if file_type == "csv":

        wget.download(url, f"data/bronze/{file_name}", timeout=timeout)

    elif file_type == "zip":

        wget.download(url, f"data/bronze/{file_name.split('.')[0]}.zip", timeout=timeout)

        unziped_file_name = unzip_file(f"data/bronze/{file_name.split('.')[0]}.zip", "data/bronze/")

        os.rename(f"data/bronze/{unziped_file_name}", f"data/bronze/{file_name}")

    saved_path = f"data/bronze/{file_name}"

    logger.info(f"File downloaded and saved in {saved_path}")

    return f"data/bronze/{file_name}"


def unzip_file(input_file, output_file):

    with zipfile.ZipFile(input_file, "r") as file:

        file.extractall(output_file)
        unziped_file_name = file.namelist()

    return unziped_file_name[0]
