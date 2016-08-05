from exceptions import NoWorkFlowSessionEntered
from exceptions import InvalidWorkflowTemplate
from exceptions import ReturnArgKeyNotPresent
from exceptions import ArgKeyNotPresent
from exceptions import StorageKeyNotPresent
from exceptions import CannotEnterSession


class GenericWorkflowStackSession(object):

    NAME_KEY = 'name'

    ALLOWED_ARGS_KEY = 'allowed_args'

    ALLOWED_STORAGE_KEY = 'allowed_storage_keys'

    ALLOWED_RETURN_VALUES_KEY = 'allowed_ret_values_keys'

    RELATIVE_SID_KEY = 'relative_sid'

    def __init__(self, starting_sid, stack_session_instance, workflow_template):
        self._stack_session = stack_session_instance
        self._starting_sid = starting_sid
        if not self._is_workflow_template_valid(workflow_template):
            raise InvalidWorkflowTemplate()
        self._sessions_by_order, self._sessions_by_key = self._index_sessions(workflow_template)

    def _is_workflow_template_valid(self, workflow_template):
        for session in workflow_template:
            if self.NAME_KEY not in session:
                return False
            if self.ALLOWED_ARGS_KEY not in session:
                return False
            if self.ALLOWED_RETURN_VALUES_KEY not in session:
                return False
            if self.ALLOWED_STORAGE_KEY not in session:
                return False

            if not isinstance(session[self.NAME_KEY], str):
                return False
            if not isinstance(session[self.ALLOWED_ARGS_KEY], list):
                return False
            if not isinstance(session[self.ALLOWED_RETURN_VALUES_KEY], list):
                return False
            if not isinstance(session[self.ALLOWED_STORAGE_KEY], list):
                return False

        return True

    def _index_sessions(self, workflow_template):
        sessions_by_order = workflow_template
        sessions_by_key = {}
        index = 0

        for current_session in sessions_by_order:
            sessions_by_key[current_session[self.NAME_KEY]] = current_session
            current_session[self.RELATIVE_SID_KEY] = index
            index += 1

        return sessions_by_order, sessions_by_key

    def is_in_session(self, session_name):
        session_info = self._sessions_by_key.get(session_name)
        if session_info is None:
            return False
        relative_sid = session_info[self.RELATIVE_SID_KEY]
        current_relative_sid, _, current_session = self._get_current_session()
        if current_session is None:
            raise NoWorkFlowSessionEntered()
        return current_relative_sid == relative_sid

    def store_in_current_session(self, key, val):
        _, session_name, session = self._get_current_session()
        if session is None:
            raise NoWorkFlowSessionEntered()
        if key not in self._sessions_by_key[session_name][self.ALLOWED_STORAGE_KEY]:
            raise StorageKeyNotPresent(key)
        session[key] = val

    def get_current_session_args(self):
        _, session_name, session = self._get_current_session()
        if session is None:
            raise NoWorkFlowSessionEntered()
        recorded_args = {}
        for arg_key in self._sessions_by_key[session_name][self.ALLOWED_ARGS_KEY]:
            recorded_args[arg_key] = session[arg_key]
        return recorded_args

    def enter_session(self, session_name, args):
        if not self._is_entering_allowed(session_name):
            raise CannotEnterSession()

        recorded_args = {}
        for key in self._sessions_by_key[session_name][self.ALLOWED_ARGS_KEY]:
            if key not in args:
                raise ArgKeyNotPresent(key)
            recorded_args[key] = args[key]

        _, _, next_session = self._stack_session.push_session()

        _, current_session_name, _ = self._get_current_session()
        for key in self._sessions_by_key[current_session_name][self.ALLOWED_ARGS_KEY]:
            next_session[key] = recorded_args[key]

    def exit_session(self, return_values):
        recorded_return_val = {}

        current_relative_sid, current_session_name, current_session = self._get_current_session()
        if current_session is None:
            raise NoWorkFlowSessionEntered()

        if current_relative_sid == self._starting_sid:
            self._stack_session.pop_session()
            return None

        for ret_val_key in self._sessions_by_key[current_session_name][self.ALLOWED_RETURN_VALUES_KEY]:
            if ret_val_key not in current_session:
                return ReturnArgKeyNotPresent(ret_val_key)
            recorded_return_val[ret_val_key] = return_values[ret_val_key]

        self._stack_session.pop_session()
        _, _, previous_session = self._get_current_session()

        for key in self._sessions_by_key[current_session_name][self.ALLOWED_RETURN_VALUES_KEY]:
            previous_session[key] = recorded_return_val[key]
        return recorded_return_val

    def _is_entering_allowed(self, session_name):
        if self._sessions_by_key.get(session_name) is None:
            return False

        current_relative_sid, _, current_session = self._get_current_session()
        if current_session is None:
            global_sid, _ = self._stack_session.get_current_session()
            if global_sid != self._starting_sid - 1 or \
                    self._sessions_by_key.get(session_name)[self.RELATIVE_SID_KEY] != 0:
                return False
        elif self._sessions_by_key.get(session_name)[self.RELATIVE_SID_KEY] != current_relative_sid + 1:
            return False

        return True

    def _get_current_session(self):
        current_global_sid, current_session = self._stack_session.get_current_session()
        if current_session is None:
            return None, None, None
        if (self._starting_sid + len(self._sessions_by_order)) <= current_global_sid or \
                self._starting_sid > current_global_sid:
            return None, None, None
        relative_sid = current_global_sid - self._starting_sid
        return relative_sid, self._sessions_by_order[relative_sid][self.NAME_KEY], current_session
