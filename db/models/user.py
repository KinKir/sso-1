from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from db.meta import Base
from db.utils import guid

from db.models.user_organization_association import user_organization_association


class User(Base):
    __tablename__ = 'users'

    id = Column(guid.GUID(), primary_key=True)
    first_name = Column(String(512), nullable=False)
    last_name = Column(String(512), nullable=True)

    email = Column(String(512), nullable=False, index=True, unique=True)
    email_verified = Column(Boolean, nullable=False)

    phone_number = Column(String(20), nullable=True, index=True, unique=True)
    phone_number_verified = Column(Boolean, nullable=True)

    user_name = Column(String(1024), nullable=False, index=True, unique=True)

    tenant_id = Column(guid.GUID(), ForeignKey('tenants.id'), nullable=False)
    tenant = relationship('Tenant', back_populates='users')

    user_accounts = relationship('UserAccount', back_populates='user')

    organizations = relationship('Organization', secondary=user_organization_association, back_populates='users')

    sessions = relationship('UserSession', back_populates='user')

    refresh_token_sessions = relationship('RefreshTokenSession', back_populates='user')

    oauth_2_codes = relationship('OAuth2Code', back_populates='user')

