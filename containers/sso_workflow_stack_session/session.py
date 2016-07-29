

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
        self.__starting_sid = starting_sid

    def is_in_session(self, session_name):
        pass

    def store_in_current_session(self, key, val):
        pass

    def get_current_session_args(self):
        pass

    def transition_to_session(self, session_name, args):
        pass

    def exit_current_session(self):
        pass

    def get_raw_data(self):
        pass

