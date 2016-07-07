#!/usr/bin/python

import sys
from db.engine_factory import create_engine
from db.meta import Base

if __name__ == '__main__':
    conn_string = sys.argv[1]
    engine = create_engine(conn_string, True)
    Base.metadata.create_all(engine)
    sys.exit(0)
else:
    print('Not a library module. Use it for creating tables for sso.')

