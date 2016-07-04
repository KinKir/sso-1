from sqlalchemy import Column, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from db.meta import Base
from db.utils import guid


class UserAccount(Base):
    __tablename__ = 'user_accounts'

    id = Column(guid.GUID(), primary_key=True)
    first_name = Column(String(512), nullable=False)
    last_name = Column(String(512), nullable=True)

    email = Column(String(512), nullable=False, index=True, unique=True)
    email_verified = Column(Boolean, nullable=False)

    phone_number = Column(String(15), nullable=True)
    phone_number_verified = Column(Boolean, nullable=True)

    user_id = Column(guid.GUID(), ForeignKey('users.id'), index=True, unique=True)
    user = relationship('User', back_populates='user_accounts')

    user_account_extra_data = relationship('UserAccountExtraData', back_populates='user_account')

