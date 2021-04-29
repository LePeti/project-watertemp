import pandas as pd
from sqlalchemy import create_engine

alchemyEngine = create_engine("postgresql+psycopg2://postgres@localhost:5432/postgres")

dbConnection = alchemyEngine.connect()

foo = pd.read_sql("select * from re_data", dbConnection)
bar = pd.read_sql("select * from re_data_cleaned", dbConnection)

dbConnection.close()
