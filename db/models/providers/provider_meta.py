from sqlalchemy import Column, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from db.meta import Base
from db.utils import guid


class ProviderMeta(Base):
    __tablename__ = 'provider_metas'

    id = Column(guid.GUID(), ForeignKey('providers.id'), primary_key=True)
    logo = Column(String(2048), nullable=False)
    name = Column(String(512), nullable=False)

    provider = relationship('Provider', back_populates='meta')

