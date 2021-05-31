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

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    title="Water temp",
)

water_temps = query_water_temps_unique()

app.layout = html.Div(
    [
        html.H1(children="Historical natural water temperatures"),
        dcc.Dropdown(
            id="name-of-water-selector",
            options=[
                {"label": water, "value": water}
                for water in pd.unique(water_temps["name_of_water"].values)
            ],
            value="Magyar tavak",
        ),
        dcc.Dropdown(
            id="location-selector",
            multi=True,
        ),
        html.Br(),
        dcc.Graph(id="water-temp-time-series-graph"),
        html.Hr(),
        html.Div(
            [
                "Source: ",
                html.A(
                    "https://www.eumet.hu/vizhomerseklet/",
                    href="https://www.eumet.hu/vizhomerseklet/",
                ),
                ". Scraped daily at 10 am UTC.",
            ],
        ),
        html.Div(
            [
                "Created by Peter Lukacs. Reach out at ",
                html.A(
                    "lukacs.peter.andras@gmail.com",
                    href="mailto:lukacs.peter.andras@gmail.com",
                ),
                ".",
            ]
        ),
    ]
)


@app.callback(
    Output("water-temp-time-series-graph", "figure"),
    Input("name-of-water-selector", "value"),
    Input("location-selector", "value"),
)
def filter_fig(name_of_water_filter, locations_filter):
    selected_waters = (
        water_temps[["name_of_water", "location", "water_temp_celsius", "date_published"]]
        .loc[
            (water_temps["name_of_water"] == name_of_water_filter)
            & (water_temps["location"].isin(locations_filter))
        ]
        .sort_values(by="date_published")
    )

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


@app.callback(
    Output("location-selector", "options"),
    Input("name-of-water-selector", "value"),
)
def populate_location_dropdown_options(name_of_water):
    locations = pd.unique(
        water_temps.loc[water_temps["name_of_water"] == name_of_water]["location"].values
    )
    return [{"label": location, "value": location} for location in locations]


@app.callback(
    Output("location-selector", "value"),
    Input("name-of-water-selector", "value"),
)
def populate_location_dropdown_values(name_of_water):
    locations = pd.unique(
        water_temps.loc[water_temps["name_of_water"] == name_of_water]["location"].values
    )
    return [location for location in locations]


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=port)
