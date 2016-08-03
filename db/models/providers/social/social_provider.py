from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

from db.meta import Base
from db.utils import guid


class SocialProvider(Base):
    __tablename__ = 'social_providers'

    id = Column(guid.GUID(), primary_key=True)
    provider_class = Column(String, index=True, nullable=False)

    meta = relationship('SocialProviderMeta', uselist=False, back_populates='provider')
    configurations = relationship('SocialProviderConfiguration', back_populates='provider')

    tenant_id = Column(guid.GUID(), ForeignKey('tenants.id'), nullable=False)
    tenant = relationship('Tenant', back_populates='social_providers')


