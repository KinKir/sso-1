from sqlalchemy import Column, BigInteger, Binary

from db.meta import Base
from db.utils import guid


class Key(Base):
    __tablename__ = 'keys'

    id = Column(guid.GUID(), primary_key=True)

    key = Column(Binary, nullable=False)
    ref_count = Column(BigInteger, nullable=False, default=0)

    expires_at = Column(BigInteger, nullable=False)
    created_at = Column(BigInteger, nullable=False)



