import requests
import pandas as pd
from bs4 import BeautifulSoup


URL = "https://www.eumet.hu/vizhomerseklet/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
tables = soup.find_all("table", class_="sportho")
dfs = pd.read_html(URL, flavor="bs4", header=0, index_col=0)
