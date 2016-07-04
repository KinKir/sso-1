from sqlalchemy import Column, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from db.meta import Base
from db.utils import guid


class ProviderMeta(Base):
    id = Column(guid.GUID(), primary_key=True)
    logo = Column(String(2048), nullable=True)
    name = Column(String(512), nullable=False)

    provider_id = Column(guid.GUID, ForeignKey('provider.id'))
    provider = relationship('Provider', back_populates='meta')

