from sqlalchemy import create_engine as create_db_engine


def create_engine(uri, echo):
    return create_db_engine(uri, echo=echo)
