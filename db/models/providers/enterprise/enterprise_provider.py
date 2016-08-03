from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

from db.meta import Base
from db.utils import guid


class EnterpriseProvider(Base):
    __tablename__ = 'enterprise_providers'

    id = Column(guid.GUID(), primary_key=True)
    provider_class = Column(String, index=True, nullable=False)

    meta = relationship('EnterpriseProviderMeta', uselist=False, back_populates='provider')
    configurations = relationship('EnterpriseProviderConfiguration', back_populates='provider')

    tenant_id = Column(guid.GUID(), ForeignKey('tenants.id'), nullable=False)
    tenant = relationship('Tenant', back_populates='enterprise_providers')

    organization_id = Column(guid.GUID(), ForeignKey('organizations.id'), nullable=False)
    organization = relationship('Organization', back_populates='enterprise_providers')


