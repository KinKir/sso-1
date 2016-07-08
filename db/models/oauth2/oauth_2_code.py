from sqlalchemy import Column, String, BigInteger
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from db.meta import Base
from db.utils import guid


class OAuth2Code(Base):
    __tablename__ = 'oauth_2_codes'

    id = Column(guid.GUID(), primary_key=True)
    code = Column(String(256), index=True, unique=True, nullable=False)
    expires_at = Column(BigInteger, nullable=False)
    created_at = Column(BigInteger, nullable=False)

    client_id = Column(guid.GUID(), ForeignKey('clients.id'), nullable=False)
    client = relationship('Client', back_populates='oauth_2_codes')
