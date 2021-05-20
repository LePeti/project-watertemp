import logging
import sys

import pandas as pd
from sqlalchemy import create_engine

from src.functions.db import concat_local_conn_string

print(sys.path)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    if len(sys.argv) == 1:  # No arguments provided (only the path to the script)
        query_string = "SELECT * FROM postgres.public.water_temp_raw"
    else:
        query_string = sys.argv[1]

    logging.info(f"Query string: {query_string}")

    db_string = concat_local_conn_string()

    engine = create_engine(db_string)
    try:
        with engine.connect() as con:
            print(pd.read_sql(query_string, con))
    except Exception as err:
        logging.error("Couldn't establish connection with the db.")
        logging.error(err)
