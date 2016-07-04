from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from db.meta import Base
from db.utils import guid


class MobileUserSession(Base):
    __tablename__ = 'mobile_user_sessions'
    id = Column(guid.GUID, primary_key=True)

    mobile_client_id = Column(guid.GUID(), ForeignKey('mobile_clients.id'), nullable=False)
    mobile_client = relationship('MobileClient', back_populates='mobile_user_sessions')
