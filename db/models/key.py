from sqlalchemy import Column, BigInteger, String

from db.meta import Base
from db.utils import guid


class Key(Base):
    __tablename__ = 'keys'

    KEY_LENGTH = 32
    SALT_LENGTH = 32
    IV_LENGTH = 12

    id = Column(guid.GUID(), primary_key=True)

    encrypted_key = Column(String(KEY_LENGTH), nullable=False)
    ref_count = Column(BigInteger, nullable=False, default=0)
    salt = Column(String(SALT_LENGTH), nullable=False)
    iv = Column(String(IV_LENGTH), nullable=False)

    expires_at = Column(BigInteger, nullable=False)
    created_at = Column(BigInteger, nullable=False)



