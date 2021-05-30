import logging
import os
import sys

import pandas as pd
from sqlalchemy import create_engine

from src.functions.db import concat_conn_string

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    if len(sys.argv) == 1:  # No arguments provided (only the path to the script)
        table_name = "water_temp_raw"
    else:
        table_name = sys.argv[1]

    logging.info(
        f"Started deleting rows from DB '{os.getenv('PG_DB_NAME')}', "
        f"table '{table_name}'."
    )

    engine = create_engine(concat_conn_string())
    try:
        with engine.connect() as con:
            num_rows = pd.read_sql(f"SELECT COUNT(*) FROM {table_name}", con).values[0][0]
            con.execute(f"DELETE FROM {table_name}")
        logging.info(f"Deleted all ({num_rows}) rows from table '{table_name}'.")
    except Exception as err:
        logging.error("Couldn't establish connection with the db.")
        logging.error(err)
