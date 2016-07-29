class SSOWorkflowStackSession(object):
    SESSION_ORDER = ['SSO_SESSION', 'PROVIDER_SESSION', 'PROVIDER_INSTANCE_SESSION']

    SESSIONS = {
        'SSO_SESSION': {
            'RELATIVE_SID': 1,
            'ARGS': ['pcr'],
            'STORAGE_KEYS': [],
            'RET_VAL_KEYS': ['uid']
        },
        'PROVIDER_SESSION': {
            'RELATIVE_SID': 2,
            'ARGS': ['pid'],
            'STORAGE_KEYS': [],
            'RET_VAL_KEYS': ['udp']
        },
        'PROVIDER_INSTANCE_SESSION': {
            'RELATIVE_SID': 3,
            'ARGS': [],
            'STORAGE_KEYS': [],
            'RET_VAL_KEYS': ['udp']
        }
    }

    ID = 'sso'

    def __init__(self, starting_sid, stack_session_instance):
        self._stack_session = stack_session_instance
        self._starting_sid = starting_sid

    def is_in_session(self, session_name):
        session_info = self.SESSIONS.get(session_name)
        if session_info is None:
            return False
        relative_sid = session_info['RELATIVE_SID']
        current_session_relative_sid, _, _ = self._get_current_session()
        return current_session_relative_sid == relative_sid

    def store_in_current_session(self, key, val):
        pass

    def get_current_session_args(self):
        pass

    def transition_to_session(self, session_name, args):
        if not self.is_transition_allowed(session_name):
            pass  # Raise an error

        recorded_return_val = {}
        _, current_session_name, current_session = self._stack_session.get_current_session()

        for ret_val_key in self.SESSIONS[current_session_name]['RET_VAL_KEYS']:
            if ret_val_key not in current_session:
                pass  # Raise an error
            recorded_return_val[ret_val_key] = current_session[ret_val_key]

        for arg_key in self.SESSIONS[current_session_name]['']:
            if arg_key not in args:
                pass  # Raise an error

        _, next_session = self._stack_session.push_session()

        for key in recorded_return_val:
            next_session[key] = recorded_return_val[key]
        for key in args:
            next_session[key] = recorded_return_val[key]

    def get_raw_data(self):
        pass

    def is_transition_allowed(self, session_name):
        current_relative_sid, _, _ = self._get_current_session()
        if self.SESSIONS.get(session_name) is None:
            return False
        if self.SESSIONS.get(session_name)['RELATIVE_SID'] != current_relative_sid + 1:
            return False
        return True

    def _get_current_session(self):
        current_sid, current_session = self._stack_session.get_current_session()
        if (self._starting_sid + len(self.SESSION_ORDER)) < current_sid:
            return None, None
        relative_sid = current_sid - self._starting_sid
        return relative_sid, self.SESSION_ORDER[relative_sid - 1], current_session
