from sqlalchemy import Column, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from db.meta import Base
from db.utils import guid


class SSOSessionExtraData(Base):
    __tablename__ = 'sso_session_extra_data'

    key = Column(String(512), primary_key=True)
    value = Column(String, nullable=False)

    sso_session_id = Column(guid.GUID(), ForeignKey('sso_sessions.id'), primary_key=True)
    sso_session = relationship('SSOSession', back_populates='sso_session_extra_data')
