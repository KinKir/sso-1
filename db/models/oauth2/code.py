from sqlalchemy import Column, String, BigInteger
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from db.meta import Base
from db.utils import guid

# Impersonation flags
IMPERSONATION_INFO_IS_IMPERSONATED = 2


class OAuth2Code(Base):
    __tablename__ = 'oauth_2_codes'

    id = Column(guid.GUID(), primary_key=True)
    code_hash = Column(String(128), index=True, unique=True, nullable=False)
    expires_at = Column(BigInteger, nullable=False)
    created_at = Column(BigInteger, nullable=False)

    redirect_uri = Column(String(2000), nullable=False)

    impersonation_info = Column(BigInteger, nullable=False)

    client_id = Column(guid.GUID(), ForeignKey('oauth_2_clients.id'), nullable=False)
    client = relationship('OAuth2Client', back_populates='codes')

    user_id = Column(guid.GUID(), ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='oauth_2_codes')
