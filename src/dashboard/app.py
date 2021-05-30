import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dotenv import load_dotenv
from src.functions.db import query_water_temps_unique_heroku

load_dotenv()
port = int(os.environ.get("PORT", 8050))

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {"background": "#111111", "text": "#7FDBFF"}

water_temps = query_water_temps_unique_heroku()

hun_waters = water_temps.loc[water_temps["name_of_water"] == "Magyar tavak"][
    ["location", "water_temp_celsius", "date_published"]
].sort_values(by="date_published")

fig = px.line(hun_waters, x="date_published", y="water_temp_celsius", color="location")

app.layout = html.Div(
    children=[
        html.H1(children="Hungarian water temperatures"),
        dcc.Graph(id="example-graph-2", figure=fig),
    ],
)

if __name__ == "__main__":
    app.run_server(debug=False, host="0.0.0.0", port=port)
