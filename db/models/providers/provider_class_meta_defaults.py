from sqlalchemy import Column, String

from db.meta import Base


class ProviderClassMetaDefaults(Base):
    provider_class = Column(String, primary_key=True)
    logo = Column(String(2048), nullable=True)
    name = Column(String(512), nullable=False)


