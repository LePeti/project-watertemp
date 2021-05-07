import logging
import os

import pandas as pd
from sqlalchemy import create_engine

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    db_string = (
        f"postgresql+psycopg2://"
        f"{os.getenv('PG_USER_NAME')}:{os.getenv('PG_PASSWORD')}@"
        f"{os.getenv('PG_HOST_NAME')}:{os.getenv('PG_PORT')}/"
        f"{os.getenv('PG_DB_NAME')}"
    )

    logging.info(
        f"Started deleting rows from DB '{os.getenv('PG_DB_NAME')}', "
        f"table 'water_temp_raw'."
    )

    engine = create_engine(db_string)
    try:
        with engine.connect() as con:
            num_rows = pd.read_sql("SELECT COUNT(*) FROM water_temp_raw", con).values[0][
                0
            ]
            con.execute("DELETE FROM water_temp_raw")
        logging.info(f"Deleted all ({num_rows}) rows from table 'water_temp_raw'.")
    except Exception as err:
        logging.error("Couldn't establish connection with the db.")
        logging.error(err)
