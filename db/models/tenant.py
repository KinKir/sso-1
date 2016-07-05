from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from db.meta import Base
from db.utils import guid


class Tenant(Base):
    __tablename__ = 'tenants'

    id = Column(guid.GUID(), primary_key=True)
    logo = Column(String(2048), nullable=False)
    name = Column(String(512), nullable=False)
    html = Column(String, nullable=True)
    css = Column(String, nullable=True)

    organizations = relationship('Organization', back_populates='tenant')
    providers = relationship('Provider', back_populates='tenant')

    tenant_extra_data = relationship('TenantExtraData', back_populates='tenant')

