from sqlalchemy import Column, BigInteger, Enum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from db.meta import Base
from db.utils import guid

import enum


class SSOSessionType(enum.Enum):
    mobile = 'Mobile'
    web = 'Web'
    unknown = 'Unknown'


class SSOSession(Base):
    __tablename__ = 'sso_sessions'

    id = Column(guid.GUID, primary_key=True)
    expires_at = Column(BigInteger, nullable=False)
    created_at = Column(BigInteger, nullable=False)

    user_id = Column(guid.GUID(), ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='sso_sessions')

    session_type = Column(Enum(SSOSessionType), nullable=False)

    sso_session_extra_data = relationship('SSOSessionExtraData', back_populates='sso_session',
                                          cascade='all, delete, delete-orphan')

    # OAuth 2 specific
    oauth_2_user_sessions = relationship('OAuth2UserSession', back_populates='sso_session',
                                         cascade='all, delete, delete-orphan')
