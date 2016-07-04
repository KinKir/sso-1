from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from db.meta import Base
from db.utils import guid


class WebClient(Base):
    __tables__ = 'web_clients'
    id = Column(guid.GUID(), primary_key=True)
    secret_hash = Column(String(64), nullable=False)
    redirect_uris = Column(String, nullable=False)
    provider_restrictions_class = Column(String, nullable=True)

    web_oauth_2_codes = relationship('WebOAuth2Code', back_populates='web_client')
    mobile_clients = relationship('MobileClient', back_populates='web_client')
    web_user_sessions = relationship('WebUserSession', back_populates='web_client')
