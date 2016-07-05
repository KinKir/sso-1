from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

from db.meta import Base
from db.utils import guid


class Provider(Base):
    __tablename__ = 'providers'

    id = Column(guid.GUID(), primary_key=True)
    provider_class = Column(String, index=True, nullable=False)

    meta = relationship('ProviderMeta', use_lists=False, back_populates='provider')
    configurations = relationship('ProviderConfiguration', back_populates='provider')

    tenant_id = Column(guid.GUID(), ForeignKey('tenants.id'), nullable=False)
    tenant = relationship('Tenant', back_populates='providers')


