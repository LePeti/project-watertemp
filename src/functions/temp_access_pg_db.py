import pandas as pd
from sqlalchemy import create_engine
import os


# Connecto to the database
db_string = "postgresql://{}:{}@{}:{}/{}".format(
    os.getenv("PG_DB_NAME"),
    os.getenv("PG_PASSWORD"),
    os.getenv("PG_HOST_NAME"),
    os.getenv("PG_PORT"),
    os.getenv("PG_USER_NAME"),
)

db = create_engine(db_string)

dbConnection = db.connect()

dummy_table = pd.DataFrame({"col_1": [1, 2, 3], "col_2": ["a", "b", "c"]})

dummy_table.to_sql("dummy_table", dbConnection, index=False, if_exists="replace")

pd.read_sql("select * from dummy_table", dbConnection)
