from exceptions import NoWorkFlowSessionEntered
from exceptions import InvalidWorkflowTemplate
from exceptions import ReturnArgKeyNotPresent
from exceptions import ArgKeyNotPresent
from exceptions import StorageKeyNotAllowed
from exceptions import CannotEnterSession
from exceptions import InvalidArguments

WORKFLOW_TEMPLATE = [
    [{
            'name': 'oauth2',
            'allowed_argument_keys': [],
            'allowed_return_value_keys': [],
            'allowed_storage_keys': [],
            'endpoints': [
                {
                    'name': 'auth',
                    'restrictions': {
                        'entry_point': True,
                        'exit_point': False,
                        'return_point': False,
                        'call_point': True,
                        'direct_access_allowed': True,
                        'allowed_storage_keys': [],
                        'is_dead_end': False
                    }
                },
                {
                    'name': 'submit',
                    'restrictions': {
                        'entry_point': False,
                        'exit_point': True,
                        'return_point': True,
                        'call_point': False,
                        'direct_access_allowed': False,
                        'allowed_storage_keys': [],
                        'is_dead_end': False
                    }
                }
            ]
        }],
    [{
            'name': 'sso',
            'allowed_argument_keys': [],
            'allowed_return_value_keys': [],
            'allowed_storage_keys': [],
            'endpoints': [
                {
                    'name': 'login',
                    'restrictions': {
                        'entry_point': True,
                        'exit_point': False,
                        'return_point': False,
                        'call_point': True,
                        'direct_access_allowed': True,
                        'allowed_storage_keys': [],
                        'is_dead_end': False
                    }
                },
                {
                    'name': 'submit',
                    'restrictions': {
                        'entry_point': False,
                        'exit_point': True,
                        'return_point': True,
                        'call_point': False,
                        'direct_access_allowed': False,
                        'allowed_storage_keys': [],
                        'is_dead_end': False
                    }
                }
            ]
        }],
    [{
        'name': 'provider',
        'allowed_argument_keys': [],
        'allowed_storage_keys': [],
        'allowed_return_value_keys': [],
        'endpoints': [
                {
                    'name': 'choose_provider',
                    'restrictions': {
                        'entry_point': True,
                        'exit_point': False,
                        'return_point': False,
                        'call_point': False,
                        'direct_access_allowed': True,
                        'can_go_to': [1, 2],
                        'allowed_storage_keys': [],
                        'is_dead_end': False
                    }
                },
                {
                    'name': 'choose_social_provider',
                    'restrictions': {
                        'entry_point': False,
                        'exit_point': False,
                        'return_point': False,
                        'call_point': True,
                        'must_arrive_from': [0],
                        'direct_access_allowed': True,
                        'allowed_storage_keys': [],
                        'is_dead_end': False
                    }
                },
                {
                    'name': 'choose_enterprise_tenant',
                    'restrictions': {
                        'entry_point': False,
                        'exit_point': False,
                        'return_point': False,
                        'call_point': False,
                        'can_go_to': [3],
                        'must_arrive_from': [0],
                        'direct_access_allowed': True,
                        'allowed_storage_keys': [],
                        'is_dead_end': False
                    }
                },
                {
                    'name': 'choose_enterprise_provider',
                    'restrictions': {
                        'entry_point': False,
                        'exit_point': False,
                        'return_point': False,
                        'call_point': True,
                        'must_arrive_from': [0, 2],
                        'direct_access_allowed': False,
                        'allowed_storage_keys': [],
                        'is_dead_end': False
                    }
                },
                {
                    'name': 'submit',
                    'restrictions': {
                        'entry_point': False,
                        'exit_point': True,
                        'return_point': True,
                        'call_point': False,
                        'direct_access_allowed': False,
                        'allowed_storage_keys': [],
                        'is_dead_end': False
                    }
                }
            ]
        }],
    []
]


class GenericWorkflowStackSession(object):

    SESSION_NAME_KEY = 'name'

    SESSION_RESTRICTIONS_KEY = 'restrictions'

    SESSION_ALLOWED_ARGS_KEY = 'allowed_argument_keys'

    SESSION_ALLOWED_STORAGE_KEY = 'allowed_storage_keys'

    SESSION_ALLOWED_RETURN_VALUES_KEY = 'allowed_return_values_keys'

    SESSION_ENDPOINT_KEY = 'endpoints'

    SESSION_ENDPOINT_NAME_KEY = 'name'

    SESSION_ENDPOINT_RESTRICTION_KEY = 'restrictions'

    SESSION_ENDPOINT_RESTRICTION_ENTRY_POINT_KEY = 'entry_point'

    SESSION_ENDPOINT_RESTRICTION_EXIT_POINT_KEY = 'exit_point'

    SESSION_ENDPOINT_RESTRICTION_RETURN_POINT_KEY = 'return_point'

    SESSION_ENDPOINT_RESTRICTION_CALL_POINT_KEY = 'call_point'

    SESSION_ENDPOINT_RESTRICTION_DIRECT_ACCESS_ALLOWED_KEY = 'direct_access_allowed'

    SESSION_ENDPOINT_RESTRICTION_ALLOWED_STORAGE_KEY = 'allowed_storage_keys'

    SESSION_ENDPOINT_RESTRICTION_DEAD_END_KEY = 'is_dead_end'

    ERROR_RETURN_VALUE_KEY = 'r_e'

    SESSION_INDEX_KEY = 'index'

    SESSION_INDEX_ENDPOINT_INDEX_KEY = 'index'

    SESSION_INDEX_ENDPOINT_KEY = 'endpoints'

    SESSION_STORAGE_ENDPOINT_KEY = 'e'

    def __init__(self, stack_session_instance, workflow_template):
        if stack_session_instance is None:
            raise InvalidArguments('Stack session instance is None.')
        self._stack_session = stack_session_instance
        if not self._is_workflow_template_valid(workflow_template):
            raise InvalidWorkflowTemplate()
        self._workflow_template = workflow_template
        self._session_index = self._index_sessions(workflow_template)

    def _is_workflow_template_valid(self, workflow_template):
        for position in workflow_template:
            for session in position:
                if self.SESSION_NAME_KEY not in session:
                    return False
                if self.SESSION_ALLOWED_ARGS_KEY not in session:
                    return False
                if self.SESSION_ALLOWED_RETURN_VALUES_KEY not in session:
                    return False
                if self.SESSION_ALLOWED_STORAGE_KEY not in session:
                    return False

                if self.SESSION_ENDPOINT_KEY not in session:
                    return False

                endpoints = session[self.SESSION_ENDPOINT_KEY]

                for endpoint in endpoints:
                    if self.SESSION_ENDPOINT_NAME_KEY not in endpoint:
                        return False
                    if self.SESSION_ENDPOINT_RESTRICTION_KEY not in endpoint:
                        return False

                    restriction = endpoint[self.SESSION_ENDPOINT_RESTRICTION_KEY]

                    if self.SESSION_ENDPOINT_RESTRICTION_ALLOWED_STORAGE_KEY not in restriction:
                        return False
                    if self.SESSION_ENDPOINT_RESTRICTION_CALL_POINT_KEY not in restriction:
                        return False
                    if self.SESSION_ENDPOINT_RESTRICTION_ENTRY_POINT_KEY not in restriction:
                        return False
                    if self.SESSION_ENDPOINT_RESTRICTION_EXIT_POINT_KEY not in restriction:
                        return False
                    if self.SESSION_ENDPOINT_RESTRICTION_RETURN_POINT_KEY not in restriction:
                        return False
                    if self.SESSION_ENDPOINT_RESTRICTION_DIRECT_ACCESS_ALLOWED_KEY not in restriction:
                        return False
                    if self.SESSION_ENDPOINT_RESTRICTION_DEAD_END_KEY not in restriction:
                        return False
        return True

    def _index_sessions(self, workflow_template):
        session_index = {}

        for i in range(0, len(workflow_template)):
            for j in range(0, len(workflow_template[i])):
                session_index[workflow_template[i][j][self.SESSION_NAME_KEY]] = \
                    {self.SESSION_INDEX_KEY: (i, j), self.SESSION_INDEX_ENDPOINT_KEY: {}}
                current_index = session_index[workflow_template[i][j][self.SESSION_NAME_KEY]]
                endpoints_array = workflow_template[i][j][self.SESSION_ENDPOINT_KEY]

                for k in range(0, len(endpoints_array)):
                    current_index[self.SESSION_INDEX_ENDPOINT_KEY][endpoints_array[k][self.SESSION_ENDPOINT_NAME_KEY]] \
                        = {self.SESSION_INDEX_ENDPOINT_INDEX_KEY: (i, j, k)}
        return session_index

    def _get_current_session_index(self):
        current_position = self._stack_session.stack_current_position
        if current_position == -1:
            raise NoWorkFlowSessionEntered()
        return current_position, self._stack_session.get_current_session_id()

    def _get_session_index(self, session_name):
        session_index_node = self._session_index.get(session_name)
        if session_index_node is None:
            return None, None
        return session_index_node[self.SESSION_INDEX_KEY]

    def _get_current_endpoint_index(self):
        current_position, current_index = self._get_current_session_index()
        storage_container = self._stack_session.get_current_session_storage()
        endpoint_index = storage_container[self.SESSION_STORAGE_ENDPOINT_KEY]
        return current_position, current_index, endpoint_index

    def _get_endpoint_index(self, session_name, endpoint_name):
        session_index_node = self._session_index.get(session_name)
        if session_index_node is None:
            return None, None, None
        endpoint_index_node = session_index_node[self.SESSION_INDEX_ENDPOINT_KEY].get(endpoint_name)
        if endpoint_index_node is None:
            return None, None, None
        return endpoint_index_node[self.SESSION_INDEX_ENDPOINT_INDEX_KEY]

    def _get_session_restrictions(self, position, session_index):
        if position < 0 or position >= len(self._workflow_template):
            return None
        session_templates = self._workflow_template[position]
        if session_index < 0 or session_index >= len(session_templates):
            return None
        endpoint_template = session_templates[session_index]
        return endpoint_template[self.SESSION_RESTRICTIONS_KEY]

    def is_in_session(self, session_name):
        position, session_index = self._get_session_index(session_name)
        if position is None:
            return False
        current_position, current_session_index = self._get_current_session_index()
        return current_position == position and current_session_index == session_index

    def is_in_endpoint(self, session_name, endpoint_name):
        position, session_index, endpoint_index = self._get_endpoint_index(session_name, endpoint_name)
        if position is None:
            return False
        current_position, current_session_index, current_endpoint_index = self._get_current_endpoint_index()
        return current_position == position and current_session_index == session_index and \
            current_endpoint_index == endpoint_index

    def store_in_current_session(self, key, val):
        current_position, current_session_index = self._get_current_session_index()
        if current_position is None:
            raise NoWorkFlowSessionEntered()
        session_restrictions = self._get_session_restrictions(current_position, current_session_index)
        if key not in session_restrictions[self.SESSION_ALLOWED_ARGS_KEY]:
            raise StorageKeyNotAllowed(key)
        self._stack_session.store_in_current_session(key, val)

    def get_current_session_args(self):
        current_position, current_session_index = self._get_current_session_index()
        if current_position is None:
            raise NoWorkFlowSessionEntered()
        return self._stack_session.get_current_session_arguments()

    def get_previous_session_return_value(self):
        current_position, current_session_index = self._get_current_session_index()
        if current_position is None:
            raise NoWorkFlowSessionEntered()
        error_value = self._stack_session.get_current_session_storage_value(self.ERROR_RETURN_VALUE_KEY)
        if error_value is not None:
            return True, error_value
        session_restrictions = self._get_session_restrictions(current_position, current_session_index)

        recorded_return_values = {}
        for key in session_restrictions[self.SESSION_ALLOWED_RETURN_VALUES_KEY]:
            recorded_return_values[key] = self._stack_session.get_current_session_storage_value(key)

        return False, recorded_return_values

    def remove_previous_session_return_value(self):
        current_position, current_session_index = self._get_current_session_index()
        if current_position is None:
            raise NoWorkFlowSessionEntered()

        error_value = self._stack_session.get_current_session_storage_value(self.ERROR_RETURN_VALUE_KEY)
        if error_value is not None:
            self._stack_session.delete_value_in_current_session(self.ERROR_RETURN_VALUE_KEY)
            return

        session_restrictions = self._get_session_restrictions(current_position, current_session_index)
        for key in session_restrictions[self.SESSION_ALLOWED_RETURN_VALUES_KEY]:
            self._stack_session.delete_value_in_current_session(key)
        return

    def go_to_endpoint(self, endpoint_name):
        pass

    def enter_session(self, session_name, endpoint_name, args):
        pass

    def exit_session(self, return_values, is_error=False, error=None):
        pass

    def _is_entering_allowed(self, session_name):
        pass

