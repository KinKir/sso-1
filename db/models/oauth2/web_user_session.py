from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from db.meta import Base
from db.utils import guid


class WebUserSession(Base):
    id = Column(guid.GUID, primary_key=True)

    mobile_client_id = Column(guid.GUID(), ForeignKey('web_clients.id'), nullable=False)
    mobile_client = relationship('WebClient', back_populates='web_user_sessions')
