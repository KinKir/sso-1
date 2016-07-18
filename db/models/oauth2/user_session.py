from sqlalchemy import Column, String, BigInteger, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from db.meta import Base
from db.utils import guid


class OAuth2UserSession(Base):
    __tablename__ = 'oauth_2_user_sessions'

    id = Column(guid.GUID, primary_key=True)
    expires_at = Column(BigInteger, nullable=False)
    created_at = Column(BigInteger, nullable=False)
    logout_token = Column(String(128), nullable=False, index=True, unique=True)

    attached_to_sso_session = Column(Boolean, nullable=False)

    client_id = Column(guid.GUID(), ForeignKey('oauth_2_clients.id'), nullable=False)
    client = relationship('OAuth2Client', back_populates='user_sessions')

    user_id = Column(guid.GUID(), ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='oauth_2_user_sessions')

    refresh_token_session_id = Column(guid.GUID(), ForeignKey('oauth_2_refresh_token_sessions.id'), nullable=False)
    refresh_token_session = relationship('OAuth2RefreshTokenSession', back_populates='user_sessions')

    sso_session_id = Column(guid.GUID(), ForeignKey('sso_sessions.id'), nullable=True)
    sso_session = relationship('SSOSession', back_populates='oauth_2_user_sessions')
