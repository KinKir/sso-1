from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from db.meta import Base
from db.utils import guid


class Tenant(Base):
    __tablename__ = 'tenants'

    id = Column(guid.GUID(), primary_key=True)
    logo = Column(String(2048), nullable=False)
    name = Column(String(512), nullable=False, unique=True, index=True)
    html = Column(String, nullable=True)
    css = Column(String, nullable=True)

    organizations = relationship('Organization', back_populates='tenant')
    social_providers = relationship('SocialProvider', back_populates='tenant')
    enterprise_providers = relationship('EnterpriseProvider', back_populates='tenant')
    users = relationship('User', back_populates='tenant')

    oauth_2_clients = relationship('OAuth2Client', back_populates='tenant')

    tenant_extra_data = relationship('TenantExtraData', back_populates='tenant')

    email_patterns = relationship('TenantEmailPattern', back_populates='tenant')

