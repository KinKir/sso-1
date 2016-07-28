from containers.generic_stack_session.session import GenericStackSession


class SSOWorkflowStackSession(object):

    ARGS_KEY = 'a'

    SESSION_ORDER = ['SSO_SESSION', 'PROVIDER_SESSION', 'PROVIDER_INSTANCE_SESSION']

    SESSIONS = {
        'SSO_SESSION': {
            'RELATIVE_SID': 1,
            'ARGS': ['pcr'],
            'VALID_STORAGE_KEYS': ['pcr'] + [ARGS_KEY]
        },
        'PROVIDER_SESSION': {
            'RELATIVE_SID': 2,
            'ARGS': ['pid'],
            'VALID_STORAGE_KEYS': ['pid'] + [ARGS_KEY]
        },
        'PROVIDER_INSTANCE_SESSION': {
            'RELATIVE_SID': 3,
            'ARGS': None,
            'VALID_STORAGE_KEYS': None
        }
    }

    ID = 'sso'

    def __init__(self, starting_sid):
        self._stack_session = GenericStackSession(self.ID)
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

