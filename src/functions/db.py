import os

import pandas as pd
from sqlalchemy import create_engine


def query_water_temps_unique_heroku():
    db_string = concat_gcp_conn_string()
    engine = create_engine(db_string)
    query_string = (
        f"SELECT * FROM {os.getenv('HEROKU_PG_DB_NAME')}.public.water_temp_unique"
    )
    with engine.connect() as con:
        return pd.read_sql(query_string, con)


def query_water_temps_unique():
    db_string = concat_gcp_conn_string()
    engine = create_engine(db_string)
    query_string = (
        f"SELECT * FROM {os.getenv('GCP_PG_DB_NAME')}.public.water_temp_unique"
    )
    with engine.connect() as con:
        water_temps = pd.read_sql(query_string, con)
    water_temps["water_temp_celsius"] = pd.to_numeric(water_temps["water_temp_celsius"])
    water_temps["date_published"] = pd.to_datetime(
        water_temps["date_published"]
    ).dt.date
    return water_temps


def query_table_stats():
    db_string = concat_gcp_conn_string()
    engine = create_engine(db_string)
    query_string = f"SELECT * FROM {os.getenv('GCP_PG_DB_NAME')}.public.table_stats"
    with engine.connect() as con:
        table_stats = pd.read_sql(query_string, con)
    table_stats["row_count"] = pd.to_numeric(table_stats["row_count"])
    table_stats["date"] = pd.to_datetime(table_stats["date"]).dt.date
    return table_stats


def concat_conn_string():
    return (
        f"postgresql+psycopg2://"
        f"{os.getenv('PG_USER_NAME')}:{os.getenv('PG_PASSWORD')}@"
        f"{os.getenv('PG_HOST_NAME')}:{os.getenv('PG_PORT')}/"
        f"{os.getenv('PG_DB_NAME')}"
    )


def concat_gcp_conn_string():
    return (
        f"postgresql+psycopg2://"
        f"{os.getenv('GCP_PG_USER_NAME')}:{os.getenv('GCP_PG_PASSWORD')}@"
        f"{os.getenv('GCP_PG_HOST_NAME')}:{os.getenv('GCP_PG_PORT')}/"
        f"{os.getenv('GCP_PG_DB_NAME')}"
    )
