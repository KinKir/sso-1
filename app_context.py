from db import SessionFactory


class SSOAppContextGlobals(object):
    def __init__(self):
        self._storage = {}
        self._session = None

    @property
    def db_session(self):
        if self._session is None:
            self._session = SessionFactory()
        return self._session

    @db_session.deleter
    def db_session(self):
        if self._session is not None:
            self._session.close()

    def get(self, name, default=None):
        return self.__dict__.get(name, default)

    def pop(self, name, default=None):
        return self.__dict__.pop(name, default)

    def setdefault(self, name, default=None):
        return self.__dict__.setdefault(name, default)

    def __contains__(self, item):
        return item in self.__dict__

    def __iter__(self):
        return iter(self.__dict__)


