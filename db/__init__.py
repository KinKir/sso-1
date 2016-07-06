from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import configure_mappers

from db.models import *
from db.engine_factory import create_engine

configure_mappers()

SessionFactory = sessionmaker()


def init_db_session_factory(uri, echo):
    SessionFactory.configure(bind=create_engine(uri, echo))

__all__ = ['SessionFactory', 'init_db_session_factory']
