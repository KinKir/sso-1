from containers.generic_session.session import GenericSession


class GenericStackSession(GenericSession):

    ARGUMENT_KEY = 'a'

    RET_VAL_KEY = 'r'

    STORAGE_KEY = 'd'

    def __init__(self):
        super(GenericSession, self).__init__()
        self[self.STORAGE_KEY] = {}
        self._next_sid = 0

    def push_session(self, args):
        current_sid = self._next_sid
        self[self.STORAGE_KEY][current_sid] = {self.ARGUMENT_KEY: args}
        self._next_sid += 1
        return self._next_sid

    def pop_session(self):
        if self._next_sid == 0:
            raise OverflowError

        current_sid = self._next_sid - 1
        ret_val = self[self.STORAGE_KEY][current_sid].get(self.RET_VAL_KEY)

        del self[self.STORAGE_KEY][current_sid]
        self._next_sid -= 1
        return ret_val

    def get_current_session(self):
        if self._next_sid == 0:
            raise OverflowError
        current_sid = self._next_sid - 1
        return self[self.STORAGE_KEY][current_sid]

    def get_current_session_args(self):
        session = self.get_current_session()
        return session.get(self.ARGUMENT_KEY)

    def get_session(self, sid):
        return self[self.STORAGE_KEY].get(sid)

    def get_session_args(self, sid):
        session = self.get_session(sid)
        return session.get(self.ARGUMENT_KEY)

    def get_max_sid_issued(self):
        return self._next_sid - 1
