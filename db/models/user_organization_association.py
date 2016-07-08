from sqlalchemy import Table, Column, ForeignKey

from db.meta import Base
from db.utils import guid

user_organization_association = Table('user_organization_associations', Base.metadata,
                                      Column('user', guid.GUID(), ForeignKey('users.id'), primary_key=True),

                                      Column('organization', guid.GUID(),
                                             ForeignKey('organizations.id'), primary_key=True)
                                      )
