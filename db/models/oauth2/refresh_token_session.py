from sqlalchemy import Column, String, BigInteger, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from db.meta import Base
from db.utils import guid


class OAuth2RefreshTokenSession(Base):
    __tablename__ = 'oauth_2_refresh_token_sessions'

    id = Column(guid.GUID, primary_key=True)
    expires_at = Column(BigInteger, nullable=False)
    created_at = Column(BigInteger, nullable=False)

    client_id = Column(guid.GUID(), ForeignKey('oauth_2_clients.id'), nullable=False)
    client = relationship('OAuth2Client', back_populates='refresh_token_sessions')

    user_id = Column(guid.GUID(), ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='oauth_2_refresh_token_sessions')

    user_sessions = relationship('OAuth2UserSession', back_populates='refresh_token_session',
                                 cascade="all, delete, delete-orphan")

