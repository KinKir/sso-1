from sqlalchemy import Column, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from db.meta import Base
from db.utils import guid


class EnterpriseProviderMeta(Base):
    __tablename__ = 'enterprise_provider_metas'

    id = Column(guid.GUID(), ForeignKey('enterprise_providers.id'), primary_key=True)
    logo = Column(String(2048), nullable=False)
    name = Column(String(512), nullable=False)

    provider = relationship('EnterpriseProvider', uselist=False, back_populates='meta')

