from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from db.meta import Base
from db.utils import guid


class WebUserSession(Base):
    __tablename__ = 'web_user_sessions'

    id = Column(guid.GUID, primary_key=True)

    web_client_id = Column(guid.GUID(), ForeignKey('web_clients.id'), nullable=False)
    web_client = relationship('WebClient', back_populates='web_user_sessions')

    user_id = Column(guid.GUID(), ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='web_sessions')
