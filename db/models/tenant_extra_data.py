from sqlalchemy import Column, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from db.meta import Base
from db.utils import guid


class TenantExtraData(Base):
    __tablename__ = 'tenant_extra_data'

    key = Column(String(512), primary_key=True)
    value = Column(String, nullable=False)

    tenant_id = Column(guid.GUID(), ForeignKey('tenants.id'), nullable=False, primary_key=True)
    tenant = relationship('Tenant', back_populates='tenant_extra_data')

