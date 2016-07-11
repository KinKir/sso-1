from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from db.meta import Base
from db.utils import guid


class Client(Base):
    __tablename__ = 'clients'
    id = Column(guid.GUID(), primary_key=True)
    secret_hash = Column(String(512), nullable=False)
    redirect_uris = Column(String, nullable=False)
    provider_restrictions_class = Column(String, nullable=True)

    oauth_2_codes = relationship('OAuth2Code', back_populates='client')
    user_sessions = relationship('UserSession', back_populates='client')
    refresh_token_sessions = relationship('RefreshTokenSession', back_populates='client')

