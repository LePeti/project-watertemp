import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
from dotenv import load_dotenv

from src.functions.db import query_water_temps_unique

load_dotenv()
port = int(os.environ.get("PORT", 8050))

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {"background": "#111111", "text": "#7FDBFF"}

water_temps = query_water_temps_unique()

app.layout = html.Div(
    [
        html.H1(children="Historical natural water temperatures"),
        dcc.Dropdown(
            id="name-of-water-selector-dropdown",
            options=[
                {"label": water, "value": water}
                for water in pd.unique(water_temps["name_of_water"].values)
            ],
            value="Magyar tavak",
        ),
        dcc.Graph(id="water-temp-time-series"),
        html.Div(
            [
                "Source: ",
                html.A(
                    "https://www.eumet.hu/vizhomerseklet/",
                    href="https://www.eumet.hu/vizhomerseklet/",
                ),
            ],
        ),
        html.Div("Scraped daily at 10 am UTC."),
        html.Div("Created by Peter Lukacs. Reach out at lukacs.peter.andras@gmail.com"),
    ]
)


@app.callback(
    Output("water-temp-time-series", "figure"),
    Input("name-of-water-selector-dropdown", "value"),
)
def filter_fig(selected_name_of_water):
    selected_waters = water_temps.loc[
        water_temps["name_of_water"] == selected_name_of_water
    ][["location", "water_temp_celsius", "date_published"]].sort_values(
        by="date_published"
    )
    selected_waters["water_temp_celsius"] = pd.to_numeric(
        selected_waters["water_temp_celsius"]
    )
    selected_waters["date_published"] = pd.to_datetime(selected_waters["date_published"])

    fig = px.line(
        selected_waters,
        x="date_published",
        y="water_temp_celsius",
        color="location",
        labels={
            "date_published": "",
            "water_temp_celsius": "water temperature (celsius)",
        },
        template="plotly_white",
    )
    fig.update_traces(mode="markers+lines")
    return fig


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=port)
