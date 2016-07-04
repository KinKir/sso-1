from sqlalchemy import Column, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from db.meta import Base
from db.utils import guid


class User(Base):
    __tablename__ = 'users'

    id = Column(guid.GUID(), primary_key=True)
    first_name = Column(String(512), nullable=False)
    last_name = Column(String(512), nullable=True)

    email = Column(String(512), nullable=False, index=True, unique=True)
    email_verified = Column(Boolean, nullable=False)

    phone_number = Column(String(15), nullable=True)
    phone_number_verified = Column(Boolean, nullable=True)

    user_name = Column(String(1024), nullable=False, index=True, unique=True)

    user_accounts = relationship('UserAccount', back_populates='user')
