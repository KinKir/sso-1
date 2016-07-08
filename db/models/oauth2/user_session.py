from sqlalchemy import Column, String, BigInteger, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from db.meta import Base
from db.utils import guid


class UserSession(Base):
    __tablename__ = 'user_sessions'

    id = Column(guid.GUID, primary_key=True)
    expires_at = Column(BigInteger, nullable=False)
    created_at = Column(BigInteger, nullable=False)
    logout_token = Column(String(128), nullable=False, index=True, unique=True)

    attached_to_auth_session = Column(Boolean, nullable=False)

    client_id = Column(guid.GUID(), ForeignKey('clients.id'), nullable=False)
    client = relationship('Client', back_populates='user_sessions')

    user_id = Column(guid.GUID(), ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='sessions')

    refresh_token_session_id = Column(guid.GUID(), ForeignKey('refresh_token_sessions.id'), nullable=False)
    refresh_token_session = relationship('RefreshTokenSession', back_populates='user_sessions')
