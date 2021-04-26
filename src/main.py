import requests
import pandas as pd
from bs4 import BeautifulSoup


URL = "https://www.eumet.hu/vizhomerseklet/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
tables = soup.find_all("table", {"class": "sportho"})
dfs = pd.read_html(URL, flavor="bs4", header=0, index_col=0)[:11]
df_names_html = soup.find_all("strong", {"class": "orszagnev"})
df_names = map(lambda x: BeautifulSoup.get_text(x).capitalize(), df_names_html)
for df_, water_name in zip(dfs, df_names):
    df_["name_of_water"] = water_name

# add name of water
# add scraping timestamp
# add last website refresh date ("Kiadva")
# Rename columns
# Column values should only include numbers
# Add logging
