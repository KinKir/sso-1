from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from db.meta import Base
from db.utils import guid


class Provider(Base):
    __tablename__ = 'providers'

    id = Column(guid.GUID(), primary_key=True)
    provider_class = Column(String, index=True, nullable=False)

    meta = relationship('ProviderMeta', use_lists=False, back_populates='provider')
    configurations = relationship('ProviderConfiguration', back_populates='provider')

