import logging
import re
from datetime import datetime

import dateparser
import pandas as pd
import requests
from bs4 import BeautifulSoup
from pytz import timezone

logging.basicConfig(level=logging.INFO)
logging.info(
    f"Started scraping at "
    f"{datetime.now(timezone('CET')).strftime('%Y-%m-%d %H:%M:%S %Z')}."
)

URL = "https://www.eumet.hu/vizhomerseklet/"
page = requests.get(URL)
if page.status_code == 200:
    logging.info(f"Requesting '{page.url}' returned status code {page.status_code}.")
else:
    logging.error(
        f"Requesting '{page.url}' returned status code {page.status_code}. "
        f"Reason: {page.reason}."
    )
time_of_scraping = datetime.now(timezone("CET")).strftime("%Y-%m-%d %H:%M:%S")
soup = BeautifulSoup(page.content, "html.parser")

date_published_text_hun = soup.find("p", text=re.compile("Kiadva.*")).get_text()
date_published_hun = date_published_text_hun[8:]
date_published = dateparser.parse(date_published_hun).strftime("%Y-%m-%d")
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

water_temp_data_tables = pd.read_html(URL, flavor="bs4", header=0, index_col=0)[:11]

names_of_waters_html = soup.find_all("strong", {"class": "orszagnev"})
names_of_waters = map(
    lambda x: BeautifulSoup.get_text(x).capitalize(), names_of_waters_html
)
if len(water_temp_data_tables) != 11 or len(names_of_waters_html) != 11:
    logging.error(
        f"11 tables were expected but found only {len(water_temp_data_tables)}."
    )
    logging.error(
        f"11 tables names were expected but found only {len(names_of_waters_html)}."
    )

for df_, water_name in zip(water_temp_data_tables, names_of_waters):
    df_["name_of_water"] = water_name

water_temp_data = pd.concat(water_temp_data_tables)

water_temp_data["time_of_scraping_cet"] = time_of_scraping
water_temp_data["date_published"] = date_published

water_temp_data.rename(
    columns={
        "cm": "water_depth_cm",
        "víz °C": "water_temp_celsius",
        "lég °C": "air_temp_celsius",
    },
    inplace=True,
)

water_temp_data.replace(to_replace=" (cm|°C)", value="", inplace=True, regex=True)

print(water_temp_data.head())

# Assertions:
#    realized I don't need this for now. You need it when you want your program
#    to stop before actually running into something unexpected. If my
#    date_published is not in the expected format, then I don't want it to stop
#    b/c it can still collect valuable information. What I want instead is to
#    log it and warn me.
# Testing
# Refactor ffs
# Add logging
