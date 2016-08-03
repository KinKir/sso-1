from sqlalchemy import Column, String, Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from db.meta import Base
from db.utils import guid

from db.models.user_organization_association import user_organization_association

# This both will be part of the 'default' tenant
ORGANIZATION_TYPE_PERSONAL = 1
ORGANIZATION_TYPE_BUSINESS = 2

# This will be part of entirely new tenant.
ORGANIZATION_TYPE_ENTERPRISE = 4


class Organization(Base):
    __tablename__ = 'organizations'

    id = Column(guid.GUID(), primary_key=True)
    logo = Column(String(2048), nullable=False)
    name = Column(String(512), nullable=False)

    flags = Column(Integer, nullable=False)

    tenant_id = Column(guid.GUID(), ForeignKey('tenants.id'), nullable=False)
    tenant = relationship('Tenant', back_populates='organizations')

    enterprise_providers = relationship('EnterpriseProvider', back_populates='organization')

    users = relationship('User', secondary=user_organization_association, back_populates='organizations')
