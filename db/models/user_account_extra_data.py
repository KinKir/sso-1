from sqlalchemy import Column, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from db.meta import Base
from db.utils import guid


class UserAccountExtraData(Base):
    __tablename__ = 'user_account_extra_data'

    key = Column(String(512), primary_key=True)
    value = Column(String, nullable=False)

    user_account_id = Column(guid.GUID(), ForeignKey('user_accounts.id'), primary_key=True)
    user_account = relationship('UserAccount', back_populates='user_account_extra_data')
