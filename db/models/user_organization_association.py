from sqlalchemy import Table, Column, ForeignKey

from db.meta import Base
from db.utils import guid

user_organization_association = Table('user_organization_associations', Base.metadata,
                                      Column(guid.GUID(), ForeignKey('users.id')),
                                      Column(guid.GUID(), ForeignKey('organizations.id'))
                                      )
