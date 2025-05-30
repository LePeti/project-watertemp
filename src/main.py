import logging
import re
from datetime import datetime

import dateparser
import pandas as pd
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pytz import timezone
from sqlalchemy import create_engine

from src.functions.db import concat_gcp_conn_string

logging.basicConfig(level=logging.DEBUG)

URL = "https://www.eumet.hu/vizhomerseklet/"


def get_watertemp_page():
    page = requests.get(URL)
    if page.status_code == 200:
        logging.info(
            f"Requesting '{page.url}' returned status code {page.status_code}."
        )
    else:
        logging.error(
            f"Requesting '{page.url}' returned status code {page.status_code}. "
            f"Reason: {page.reason}."
        )
    return page


def scrape_watertemp_tables():
    return pd.read_html(
        "https://www.eumet.hu/vizhomerseklet/", flavor="bs4", header=0, index_col=0
    )[:11]


def extract_publish_date(soup):
    date_published_text_hun = soup.find("p", string=re.compile("Kiadva.*")).get_text()
    date_published_hun = date_published_text_hun[8:]
    date_published = dateparser.parse(date_published_hun, languages=["hu"]).strftime(
        "%Y-%m-%d"
    )
    expected_date_published_format = "20\\d\\d\\. [A-zÀ-ÿ]+ \\d{1,2}\\."
    date_published_matches_expectation = bool(
        re.match(expected_date_published_format, date_published_hun)
    )
    if not date_published_matches_expectation:
        logging.warning(
            f"Publish date format is not as expected. Value was {date_published_hun} "
            f"Expectation is for example '2021. Április 22.' "
            f"Expectation regex pattern is '{expected_date_published_format}'"
        )
    else:
        logging.info(
            f"Publish date on website at the time of scraping is "
            f"{date_published} [{date_published_hun}]"
        )
    return date_published


if __name__ == "__main__":
    load_dotenv("/app/.env")

    # Scrape the water temperature data
    time_of_scraping = datetime.now(timezone("CET"))
    logging.info(
        f"Started scraping at {time_of_scraping.strftime('%Y-%m-%d %H:%M:%S %Z')}."
    )

    page = get_watertemp_page()
    soup = BeautifulSoup(page.content, "html.parser")
    date_published = extract_publish_date(soup)

    water_temp_data_tables = scrape_watertemp_tables()

    names_of_waters_html = soup.find_all("strong", {"class": "orszagnev"})
    names_of_waters = map(
        lambda x: BeautifulSoup.get_text(x).capitalize(), names_of_waters_html
    )
    if len(water_temp_data_tables) != 11 or len(names_of_waters_html) != 11:
        logging.error(
            f"11 tables were expected but found {len(water_temp_data_tables)}."
        )
        logging.error(
            f"11 tables names were expected but found {len(names_of_waters_html)}."
        )

    for df_, water_name in zip(water_temp_data_tables, names_of_waters):
        df_["name_of_water"] = water_name

    water_temp_data = pd.concat(water_temp_data_tables)
    water_temp_data.reset_index(inplace=True)
    water_temp_data.rename(columns={"index": "location"}, inplace=True)

    # Add helper columns
    water_temp_data["time_of_scraping_cet"] = time_of_scraping.strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    water_temp_data["date_published"] = date_published
    # TODO Log warning when date_published and time_of_scraping --> date mismatch
    if (num_cols := len(water_temp_data.columns)) != 7:
        logging.error(f"Expected 7 columns of data but found {num_cols}.")

    # Clean column names
    water_temp_data.rename(
        columns={
            "cm": "water_depth_cm",
            "víz °C": "water_temp_celsius",
            "lég °C": "air_temp_celsius",
        },
        inplace=True,
    )

    water_temp_data.replace(to_replace=" (cm|°C)", value="", inplace=True, regex=True)

    # Remove some water temperature data (to save db space)
    water_temp_data = water_temp_data[
        water_temp_data.name_of_water.isin(
            [
                "Magyar tavak",
                "Adriai-tenger",
                "Tengerek",
                "Tisza",
                "Duna",
                "Földközi-tenger",
            ]
        )
    ]

    try:
        logging.info(f"connection string: {concat_gcp_conn_string()}")
        engine = create_engine(concat_gcp_conn_string())
        dbConnection = engine.connect()
        logging.info("Successfully connected to database.")

        try:
            num_rows_before = pd.read_sql(
                "SELECT COUNT(*) FROM water_temp_raw LIMIT 5", dbConnection
            ).values[0][0]
            logging.info(
                f"Table 'water_temp_raw' contains {num_rows_before} before appending new "
                f"data."
            )
        except Exception as err:
            logging.warning("'water_temp_raw' does not yet exist.")
            logging.info(
                f"Creating 'water_temp_raw' and inserting "
                f"{water_temp_data.shape[0]} rows."
            )
            logging.debug(f"Error caught: {err}")
            dbConnection = engine.connect()
            water_temp_data.to_sql(
                "water_temp_raw", dbConnection, index=False, if_exists="append"
            )
        else:
            logging.info(f"Appending {water_temp_data.shape[0]} new rows.")
            dbConnection = engine.connect()
            water_temp_data.to_sql(
                "water_temp_raw", dbConnection, index=False, if_exists="append"
            )
            num_rows_after = pd.read_sql(
                "SELECT COUNT(*) FROM water_temp_raw LIMIT 5", dbConnection
            ).values[0][0]
            logging.info(
                f"Table 'water_temp_raw' contains {num_rows_after} "
                f"after appending new data."
            )
        dbConnection.close()
    except Exception as err:
        logging.error("Couldn't establish connection with the db.")
        logging.error(err)
