import os

import pandas as pd
from sqlalchemy import create_engine


def query_water_temps_unique_heroku():
    db_string = concat_heroku_conn_string()
    engine = create_engine(db_string)
    query_string = (
        f"SELECT * FROM {os.getenv('HEROKU_PG_DB_NAME')}.public.water_temp_unique"
    )
    with engine.connect() as con:
        return pd.read_sql(query_string, con)


def query_water_temps_unique():
    db_string = concat_conn_string()
    engine = create_engine(db_string)
    query_string = f"SELECT * FROM {os.getenv('PG_DB_NAME')}.public.water_temp_unique"
    with engine.connect() as con:
        return pd.read_sql(query_string, con)


def concat_conn_string():
    return (
        f"postgresql+psycopg2://"
        f"{os.getenv('PG_USER_NAME')}:{os.getenv('PG_PASSWORD')}@"
        f"{os.getenv('PG_HOST_NAME')}:{os.getenv('PG_PORT')}/"
        f"{os.getenv('PG_DB_NAME')}"
    )


def concat_heroku_conn_string():
    return (
        f"postgresql+psycopg2://"
        f"{os.getenv('HEROKU_PG_USER_NAME')}:{os.getenv('HEROKU_PG_PASSWORD')}@"
        f"{os.getenv('HEROKU_PG_HOST_NAME')}:{os.getenv('HEROKU_PG_PORT')}/"
        f"{os.getenv('HEROKU_PG_DB_NAME')}"
    )


# %%
