from sqlalchemy import Column, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from db.meta import Base
from db.utils import guid


class SocialProviderConfiguration(Base):
    __tablename__ = 'social_provider_configurations'

    key = Column(String(512), primary_key=True)
    value = Column(String, nullable=False)

    provider_id = Column(guid.GUID(), ForeignKey('social_providers.id'), primary_key=True)
    provider = relationship('SocialProvider', back_populates='configurations')
