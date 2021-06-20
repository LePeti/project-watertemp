import os
from datetime import datetime, timedelta

import dash
import flask
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
from dotenv import load_dotenv

from src.functions.db import query_water_temps_unique

load_dotenv()
port = int(os.environ.get("PORT", 8050))

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

f_app = flask.Flask(__name__)
app = dash.Dash(
    __name__, external_stylesheets=external_stylesheets, title="Water temp", server=f_app
)

water_temps = query_water_temps_unique().sort_values(
    ["name_of_water", "location", "date_published"]
)

water_temps_to_show = water_temps[
    [
        "date_published",
        "name_of_water",
        "location",
        "water_temp_celsius",
        "water_depth_cm",
    ]
]

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
        dcc.RadioItems(
            id="time-range-selector",
            options=[
                {"label": "All", "value": "365 * 3"},
                {"label": "Last 30 days", "value": "30"},
                {"label": "Last 7 days", "value": "7"},
            ],
            value="365 * 3",
            labelStyle={"display": "inline-block"},
        ),
        html.Br(),
        dcc.Graph(id="water-temp-time-series-graph"),
        dash_table.DataTable(
            id="table",
            columns=[{"name": i, "id": i} for i in water_temps_to_show.columns],
            data=water_temps_to_show.to_dict("records"),
            page_size=10,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
        ),
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
    Input("time-range-selector", "value"),
)
def filter_fig(name_of_water_filter, locations_filter, time_range_selector):
    min_date_to_show = datetime.now().date() - timedelta(days=eval(time_range_selector))
    selected_waters = (
        water_temps[["name_of_water", "location", "water_temp_celsius", "date_published"]]
        .loc[
            (water_temps["name_of_water"] == name_of_water_filter)
            & (water_temps["location"].isin(locations_filter))
            & (water_temps["date_published"] >= min_date_to_show)
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
    Output("location-selector", "value"),
    Input("name-of-water-selector", "value"),
)
def populate_location_dropdown(name_of_water):
    locations = pd.unique(
        water_temps.loc[water_temps["name_of_water"] == name_of_water]["location"].values
    )
    return (
        [{"label": location, "value": location} for location in locations],
        [location for location in locations],
    )


@app.callback(
    Output("time-range-selector", "value"),
    Input("time-range-selector", "value"),
    Input("name-of-water-selector", "value"),
    Input("location-selector", "value"),
)
def validate_time_range_selector_input(
    time_range_selector, name_of_water_filter, locations_filter
):
    min_date_to_show = datetime.now().date() - timedelta(days=eval(time_range_selector))
    filtered_dates = water_temps.loc[
        (water_temps["name_of_water"] == name_of_water_filter)
        & (water_temps["location"].isin(locations_filter))
    ]["date_published"]
    max_date_in_data = filtered_dates.max()

    if max_date_in_data >= min_date_to_show:
        return time_range_selector
    else:
        return "365 * 3"


if __name__ == "__main__":
    app.run_server(debug=False, host="0.0.0.0", port=port)
