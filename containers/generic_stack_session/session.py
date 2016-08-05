from containers.generic_session.session import GenericSession


class GenericStackSession(GenericSession):

    STORAGE_KEY = 'd'

    ARCHIVE_KEY = 'e'

    ID_KEY = 'i'

    def __init__(self, stack_id):
        super(GenericStackSession, self).__init__()
        self[self.STORAGE_KEY] = {}
        self[self.ARCHIVE_KEY] = {}
        self[self.ID_KEY] = stack_id
        self._next_sid = 0

    def push_session(self):
        current_sid = self._next_sid
        self[self.STORAGE_KEY][current_sid] = {}
        self._next_sid += 1
        return self._next_sid, current_sid, self[self.STORAGE_KEY][current_sid]

    def pop_session(self):
        if self._next_sid == 0:
            raise OverflowError

        current_sid = self._next_sid - 1
        self[self.ARCHIVE_KEY][current_sid] = self[self.STORAGE_KEY][current_sid]

        del self[self.STORAGE_KEY][current_sid]
        self._next_sid -= 1
        return self._next_sid

    def get_current_session(self):
        current_sid = self._next_sid - 1
        if current_sid == -1:
            return -1, None
        return current_sid, self[self.STORAGE_KEY][current_sid]

    def store_in_current_session(self, key, value):
        _, current_session = self.get_current_session()
        current_session[key] = value

    def get_session(self, sid):
        return self[self.STORAGE_KEY].get(sid)

    def get_max_sid_issued(self):
        return self._next_sid - 1

    def get_archived_sessions(self):
        return self[self.ARCHIVE_KEY]
