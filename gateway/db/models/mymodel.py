from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
)

from gateway.db.utils.guid import GUID

from .meta import Base


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)
    extra = Column(GUID())


Index('my_index', MyModel.name, unique=True, mysql_length=255)
