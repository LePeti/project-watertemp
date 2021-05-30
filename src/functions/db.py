import os


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
