from sqlalchemy import Column, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from db.meta import Base
from db.utils import guid


class MobileClient(Base):
    __tablename__ = 'mobile_clients'
    id = Column(guid.GUID(), primary_key=True)
    secret_hash = Column(String(64), nullable=False)
    redirect_uris = Column(String, nullable=False)
    provider_restrictions_class = Column(String, nullable=True)

    web_client_id = Column(guid.GUID(), ForeignKey('web_clients.id'), nullable=False)
    web_client = relationship('WebClient', back_populates='mobile_clients')

    mobile_oauth_2_codes = relationship('MobileOAuth2Code', back_populates='mobile_client')
    mobile_user_sessions = relationship('MobileUserSession', back_populates='mobile_client')

