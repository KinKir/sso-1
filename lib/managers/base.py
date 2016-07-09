class Manager(object):
    def __init__(self, session):
        self._session = session

    @property
    def session(self):
        return self._session

    @session.setter
    def session(self, s):
        self._session = s
