import plotly.express as px


def plot_table_stats(table_stats_df):
    fig = px.line(
        table_stats_df,
        x="date",
        y="row_count",
        color="table_name",
        labels={
            "date": "",
            "row_count": "row count",
        },
        template="plotly_white",
    )
    fig.update_traces(mode="markers+lines")
    return fig
