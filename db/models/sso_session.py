from sqlalchemy import Column, String, BigInteger, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from db.meta import Base
from db.utils import guid


class SSOSession(Base):
    __tablename__ = 'sso_sessions'

    id = Column(guid.GUID, primary_key=True)
    expires_at = Column(BigInteger, nullable=False)
    created_at = Column(BigInteger, nullable=False)

    user_id = Column(guid.GUID(), ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='sso_sessions')

    # OAuth 2 specific
    oauth_2_user_sessions = relationship('OAuth2UserSession', back_populates='sso_session',
                                         cascade="all, delete, delete-orphan")