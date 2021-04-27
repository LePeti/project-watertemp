import re
from datetime import datetime

import dateparser
import pandas as pd
import requests
from bs4 import BeautifulSoup
from pytz import timezone

URL = "https://www.eumet.hu/vizhomerseklet/"
page = requests.get(URL)
time_of_scraping = datetime.now(timezone("CET")).strftime("%Y-%m-%d %H:%M:%S")
soup = BeautifulSoup(page.content, "html.parser")

date_published_hun = soup.find("p", text=re.compile("Kiadva.*")).get_text()[8:]
date_pubished = dateparser.parse(date_published_hun).strftime("%Y-%m-%d")

water_temp_data_tables = pd.read_html(URL, flavor="bs4", header=0, index_col=0)[:11]

names_of_waters_html = soup.find_all("strong", {"class": "orszagnev"})
names_of_waters = map(
    lambda x: BeautifulSoup.get_text(x).capitalize(), names_of_waters_html
)
for df_, water_name in zip(water_temp_data_tables, names_of_waters):
    df_["name_of_water"] = water_name

water_temp_data = pd.concat(water_temp_data_tables)

water_temp_data["time_of_scraping_cet"] = time_of_scraping
water_temp_data["date_published"] = date_pubished

water_temp_data.rename(
    columns={
        "cm": "water_depth_cm",
        "víz °C": "water_temp_celsius",
        "lég °C": "air_temp_celsius",
    },
    inplace=True,
)

water_temp_data.replace(to_replace=" (cm|°C)", value="", inplace=True, regex=True)

water_temp_data.head()

# Assertions
# Testing
# Refactor ffs
# Add logging
