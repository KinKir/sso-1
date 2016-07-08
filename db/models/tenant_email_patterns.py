from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from db.meta import Base
from db.utils import guid


class TenantEmailPattern(Base):
    __tablename__ = 'tenant_email_patterns'

    pattern = Column(String, primary_key=True)
    tenant_id = Column(guid.GUID(), ForeignKey('tenants.id'), primary_key=True)

    tenant = relationship('Tenant', back_populates='email_patterns')
