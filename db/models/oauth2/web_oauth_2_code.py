from sqlalchemy import Column, String, BigInteger
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from db.meta import Base
from db.utils import guid


class WebOAuth2Code(Base):
    __table__ = 'web_oauth_2_codes'

    id = Column(guid.GUID(), primary_key=True)
    code = Column(String(256), index=True, unique=True, nullable=False)
    expires_at = Column(BigInteger, nullable=False)
    created_at = Column(BigInteger, nullable=False)

    web_client_id = Column(guid.GUID(), ForeignKey('web_clients.id'))
    web_client = relationship('WebClient', back_populates='web_oauth_2_codes')
