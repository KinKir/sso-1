from sqlalchemy import Column, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from db.meta import Base
from db.utils import guid

from db.models.user_organization_association import user_organization_association


class Organization(Base):
    __tablename__ = 'organizations'

    id = Column(guid.GUID(), primary_key=True)
    logo = Column(String(2048), nullable=False)
    name = Column(String(512), nullable=False)

    tenant_id = Column(guid.GUID(), ForeignKey('tenants.id'), nullable=False)
    tenant = relationship('Tenant', back_populates='organizations')

    users = relationship('User', secondary=user_organization_association, back_populates='organizations')
