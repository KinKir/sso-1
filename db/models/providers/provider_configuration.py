from sqlalchemy import Column, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from db.meta import Base
from db.utils import guid


class ProviderConfiguration(Base):
    key = Column(String(512), nullable=False, primary_key=True)
    value = Column(String, nullable=False)

    provider_id = Column(guid.GUID, ForeignKey('provider.id'), primary_key=True)
    provider = relationship('Provider', back_populates='meta')
