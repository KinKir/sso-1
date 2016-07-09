from sqlalchemy import Column, String, BigInteger
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from db.meta import Base
from db.utils import guid

OAUTH_2_CODE_SIZE = 256

DEFAULT_EXPIRATION_TIME_DELTA = 5*60


class OAuth2Code(Base):
    __tablename__ = 'oauth_2_codes'

    id = Column(guid.GUID(), primary_key=True)
    code = Column(String(OAUTH_2_CODE_SIZE), index=True, unique=True, nullable=False)
    expires_at = Column(BigInteger, nullable=False)
    created_at = Column(BigInteger, nullable=False)

    redirect_uri = Column(String(2000), nullable=False)

    client_id = Column(guid.GUID(), ForeignKey('clients.id'), nullable=False)
    client = relationship('Client', back_populates='oauth_2_codes')

    user_id = Column(guid.GUID(), ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='oauth_2_codes')
