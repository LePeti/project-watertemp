import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone
import dateparser
import re


URL = "https://www.eumet.hu/vizhomerseklet/"
page = requests.get(URL)

time_of_scraping = datetime.now(timezone("CET")).strftime("%Y-%m-%d %H:%M:%S")

soup = BeautifulSoup(page.content, "html.parser")
date_published_text_hun = soup.find("p", text=re.compile("Kiadva.*")).get_text()
date_published_hun = re.search(
    "\\d{1,4}\\. .+ \\d{1,2}\\.", date_published_text_hun
).group()
date_pubished = dateparser.parse(date_published_hun).strftime("%Y-%m-%d")
tables = soup.find_all("table", {"class": "sportho"})
dfs = pd.read_html(URL, flavor="bs4", header=0, index_col=0)[:11]
df_names_html = soup.find_all("strong", {"class": "orszagnev"})
df_names = map(lambda x: BeautifulSoup.get_text(x).capitalize(), df_names_html)
for df_, water_name in zip(dfs, df_names):
    df_["name_of_water"] = water_name

df_concat = pd.concat(dfs)
df_concat["time_of_scraping_cet"] = time_of_scraping
df_concat["date_published"] = date_pubished

df_concat.rename(
    columns={
        "cm": "water_depth_cm",
        "víz °C": "water_temp_celsius",
        "lég °C": "air_temp_celsius",
    },
    inplace=True,
)

df_concat.replace(to_replace=" (cm|°C)", value="", inplace=True, regex=True)

# Assertions
# Testing
# Refactor ffs
# Add logging
# add isort
