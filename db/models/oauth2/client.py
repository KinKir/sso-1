from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from db.meta import Base
from db.utils import guid


class OAuth2Client(Base):
    __tablename__ = 'oauth_2_clients'
    id = Column(guid.GUID(), primary_key=True)
    secret_hash = Column(String(512), nullable=False)
    redirect_uris = Column(String, nullable=False)
    provider_restrictions_class = Column(String, nullable=True)

    codes = relationship('OAuth2Code', back_populates='client')
    user_sessions = relationship('OAuth2UserSession', back_populates='client')
    refresh_token_sessions = relationship('OAuth2RefreshTokenSession', back_populates='client')

