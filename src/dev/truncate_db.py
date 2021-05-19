import logging
import os
import sys

import pandas as pd
from sqlalchemy import create_engine

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    if sys.argv is None:
        table_name = "water_temp_raw"
    else:
        table_name = sys.argv[1]

    db_string = (
        f"postgresql+psycopg2://"
        f"{os.getenv('PG_USER_NAME')}:{os.getenv('PG_PASSWORD')}@"
        f"{os.getenv('PG_HOST_NAME')}:{os.getenv('PG_PORT')}/"
        f"{os.getenv('PG_DB_NAME')}"
    )

    logging.info(
        f"Started deleting rows from DB '{os.getenv('PG_DB_NAME')}', "
        f"table '{table_name}'."
    )

    engine = create_engine(db_string)
    try:
        with engine.connect() as con:
            num_rows = pd.read_sql(f"SELECT COUNT(*) FROM {table_name}", con).values[0][0]
            con.execute(f"DELETE FROM {table_name}")
        logging.info(f"Deleted all ({num_rows}) rows from table '{table_name}'.")
    except Exception as err:
        logging.error("Couldn't establish connection with the db.")
        logging.error(err)
