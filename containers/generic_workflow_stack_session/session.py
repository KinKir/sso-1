from exceptions import NoWorkFlowSessionEntered
from exceptions import InvalidWorkflowTemplate
from exceptions import ReturnArgKeyNotPresent
from exceptions import ArgKeyNotPresent
from exceptions import StorageKeyNotAllowed
from exceptions import CannotEnterSession
from exceptions import InvalidArguments
from exceptions import CannotEnterEndpoint


WORKFLOW_TEMPLATE = [
    [{
            'name': 'oauth2',
            'restrictions': {
                'allowed_argument_keys': [],
                'allowed_return_value_keys': [],
                'allowed_storage_keys': []
            },
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
            'restrictions': {
                'allowed_argument_keys': [],
                'allowed_return_value_keys': [],
                'allowed_storage_keys': []
            },
            'endpoints': [
                {
                    'name': 'login',
                    'restrictions': {
                        'entry_point': True,
                        'exit_point': False,
                        'return_point': False,
                        'call_point': True,
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
                        'is_dead_end': False
                    }
                }
            ]
        }],
    [{
        'name': 'provider',
        'restrictions': {
            'allowed_argument_keys': [],
            'allowed_return_value_keys': [],
            'allowed_storage_keys': []
        },
        'endpoints': [
                {
                    'name': 'choose_provider',
                    'restrictions': {
                        'entry_point': True,
                        'exit_point': False,
                        'return_point': False,
                        'call_point': False,
                        'can_go_to': [1, 2],
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
                        'is_dead_end': False
                    }
                }
            ]
        }],
    [{
        'name': 'provider_class_local',
        'restrictions': {
            'allowed_argument_keys': [],
            'allowed_return_value_keys': [],
            'allowed_storage_keys': []
        },
        'endpoints': [
            {
                'name': 'sign_in',
                'restrictions': {
                    'entry_point': True,
                    'exit_point': True,
                    'return_point': False,
                    'call_point': False,
                    'is_dead_end': False
                }
            },
            {
                'name': 'sign_up',
                'restrictions': {
                    'entry_point': True,
                    'exit_point': False,
                    'return_point': False,
                    'call_point': False,
                    'is_dead_end': False,
                    'can_go_to': [2]
                }
            },
            {
                'name': 'send_verification_email',
                'restrictions': {
                    'entry_point': False,
                    'exit_point': False,
                    'return_point': False,
                    'call_point': False,
                    'is_dead_end': False,
                    'must_arrive_from': [1]
                }
            },
            {
                'name': 'email_verifier',
                'restrictions': {
                    'entry_point': False,
                    'exit_point': True,
                    'return_point': False,
                    'call_point': False,
                    'auto_arrive_allowed_from': [2],
                    'is_dead_end': False
                }
            },
            {
                'name': 'forget_password_init',
                'restrictions': {
                    'entry_point': False,
                    'exit_point': False,
                    'return_point': False,
                    'call_point': False,
                    'is_dead_end': False,
                    'must_arrive_from': [0]
                }
            },
            {
                'name': 'forget_password_token_consumer',
                'restrictions': {
                    'entry_point': False,
                    'exit_point': False,
                    'return_point': False,
                    'call_point': False,
                    'is_dead_end': False,
                    'auto_arrive_allowed_from': [4],
                    'can_go_to': [6]
                }
            },
            {
                'name': 'forget_password',
                'restrictions': {
                    'entry_point': False,
                    'exit_point': True,
                    'return_point': False,
                    'call_point': False,
                    'is_dead_end': False,
                    'must_arrive_from': [5]
                }
            }
        ]
    }]
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

    SESSION_ENDPOINT_RESTRICTION_AUTO_ARRIVE_ALLOWED_FROM_KEY = 'auto_arrive_allowed_from'

    SESSION_ENDPOINT_RESTRICTION_ALLOWED_STORAGE_KEY = 'allowed_storage_keys'

    SESSION_ENDPOINT_RESTRICTION_DEAD_END_KEY = 'is_dead_end'

    SESSION_ENDPOINT_RESTRICTION_MUST_COME_FROM = 'must_come_from'

    SESSION_ENDPOINT_RESTRICTION_CAN_GO_TO = 'can_go_to'

    SESSION_STORAGE_ERROR_RETURN_VALUE_KEY = 'r_e'

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

                if self.SESSION_STORAGE_ERROR_RETURN_VALUE_KEY in session[self.SESSION_ALLOWED_RETURN_VALUES_KEY]:
                    return False
                if self.SESSION_STORAGE_ERROR_RETURN_VALUE_KEY in session[self.SESSION_ALLOWED_STORAGE_KEY]:
                    return False
                if self.SESSION_STORAGE_ENDPOINT_KEY in session[self.SESSION_ALLOWED_STORAGE_KEY]:
                    return False
                if self.SESSION_STORAGE_ENDPOINT_KEY in session[self.SESSION_ALLOWED_RETURN_VALUES_KEY]:
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
                    if self.SESSION_ENDPOINT_RESTRICTION_AUTO_ARRIVE_ALLOWED_FROM_KEY not in restriction:
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

    def _get_endpoint_index(self, session_name: str, endpoint_name: str) -> tuple:
        session_index_node = self._session_index.get(session_name)
        if session_index_node is None:
            return None, None, None
        endpoint_index_node = session_index_node[self.SESSION_INDEX_ENDPOINT_KEY].get(endpoint_name)
        if endpoint_index_node is None:
            return None, None, None
        return endpoint_index_node[self.SESSION_INDEX_ENDPOINT_INDEX_KEY]

    def _get_session_info(self, position, session_index):
        if position < 0 or position >= len(self._workflow_template):
            return None, None, None
        session_templates = self._workflow_template[position]
        if session_index < 0 or session_index >= len(session_templates):
            return None, None, None

        requested_session_template = session_templates[session_index]
        return requested_session_template[self.SESSION_NAME_KEY], \
            requested_session_template[self.SESSION_RESTRICTIONS_KEY], \
            requested_session_template[self.SESSION_ENDPOINT_KEY]

    def _get_endpoint_info(self, position, session_index, endpoint_index):
        if position < 0 or position >= len(self._workflow_template):
            return None, None, None
        session_templates = self._workflow_template[position]
        if session_index < 0 or session_index >= len(session_templates):
            return None, None, None
        endpoint_templates = session_templates[session_index][self.SESSION_ENDPOINT_KEY]
        if endpoint_index < 0 or endpoint_index >= len(endpoint_templates):
            return None, None, None

        requested_endpoint_template = endpoint_templates[endpoint_index]
        return session_templates[session_index][self.SESSION_NAME_KEY], \
            requested_endpoint_template[self.SESSION_ENDPOINT_NAME_KEY], \
            requested_endpoint_template[self.SESSION_ENDPOINT_RESTRICTION_KEY]

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
        _, session_restrictions, _ = self._get_session_info(current_position, current_session_index)
        if key not in session_restrictions[self.SESSION_ALLOWED_STORAGE_KEY]:
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
        error_value = self._stack_session.get_current_session_storage_value(self.SESSION_STORAGE_ERROR_RETURN_VALUE_KEY)
        if error_value is not None:
            return True, error_value
        _, session_restrictions, _ = self._get_session_info(current_position, current_session_index)

        recorded_return_values = {}
        for key in session_restrictions[self.SESSION_ALLOWED_RETURN_VALUES_KEY]:
            recorded_return_values[key] = self._stack_session.get_current_session_storage_value(key)

        return False, recorded_return_values

    def remove_previous_session_return_value(self):
        current_position, current_session_index = self._get_current_session_index()
        if current_position is None:
            raise NoWorkFlowSessionEntered()

        error_value = self._stack_session.get_current_session_storage_value(self.SESSION_STORAGE_ERROR_RETURN_VALUE_KEY)
        if error_value is not None:
            self._stack_session.delete_value_in_current_session(self.SESSION_STORAGE_ERROR_RETURN_VALUE_KEY)
            return

        _, session_restrictions, _ = self._get_session_info(current_position, current_session_index)
        for key in session_restrictions[self.SESSION_ALLOWED_RETURN_VALUES_KEY]:
            self._stack_session.delete_value_in_current_session(key)
        return

    def auto_arrive_to_endpoint(self, endpoint_name):
        current_position, current_session_index, current_endpoint_index = self._get_current_endpoint_index()
        if current_position is None:
            raise NoWorkFlowSessionEntered()

        current_endpoint_session_name, current_endpoint_name, current_endpoint_restrictions = \
            self._get_endpoint_info(current_position, current_session_index, current_endpoint_index)

        position, session_index, next_endpoint_index = self._get_endpoint_index(current_endpoint_session_name,
                                                                                endpoint_name)

        if position is None:
            raise InvalidArguments('Endpoint does not exist or it is not part of the current session')

        _, _, next_endpoint_restrictions = self._get_endpoint_info(position, session_index, next_endpoint_index)
        if next_endpoint_restrictions[self.SESSION_ENDPOINT_RESTRICTION_AUTO_ARRIVE_ALLOWED_FROM_KEY] is not None:
            if current_endpoint_index not in \
                   next_endpoint_restrictions[self.SESSION_ENDPOINT_RESTRICTION_AUTO_ARRIVE_ALLOWED_FROM_KEY]:
                raise CannotEnterEndpoint('Endpoint does not allow auto arrive from current endpoint.')
        else:
            raise CannotEnterEndpoint('Auto arrive is not supported.')

        self._stack_session.store_in_current_session(self.SESSION_STORAGE_ENDPOINT_KEY, next_endpoint_index)

    def go_to_endpoint(self, endpoint_name):
        current_position, current_session_index, current_endpoint_index = self._get_current_endpoint_index()
        if current_position is None:
            raise NoWorkFlowSessionEntered()

        current_endpoint_session_name, current_endpoint_name, current_endpoint_restrictions = \
            self._get_endpoint_info(current_position, current_session_index, current_endpoint_index)

        position, session_index, next_endpoint_index = self._get_endpoint_index(current_endpoint_session_name,
                                                                                endpoint_name)
        if position is None:
            raise InvalidArguments('Endpoint does not exist or it is not part of the current session')
        _, _, next_endpoint_restrictions = self._get_endpoint_info(position, session_index, next_endpoint_index)

        if not self._is_entering_to_endpoint_allowed(current_endpoint_index, current_endpoint_restrictions,
                                                     next_endpoint_index, next_endpoint_restrictions):
            raise CannotEnterEndpoint()

        self._stack_session.store_in_current_session(self.SESSION_STORAGE_ENDPOINT_KEY, next_endpoint_index)

    def enter_session(self, next_session_name, next_endpoint_name, args):
        current_position, current_session_index, current_endpoint_index = self._get_current_endpoint_index()
        next_position, next_session_index, next_endpoint_index = self._get_endpoint_index(next_session_name,
                                                                                          next_endpoint_name)
        if next_position is None:
            raise CannotEnterSession('Mentioned session/endpoint does not exists')
        _, _, next_endpoint_restrictions = self._get_endpoint_info(next_position, next_session_index,
                                                                   next_endpoint_index)

        _, _, current_endpoint_restrictions = self._get_endpoint_info(current_position, current_session_index,
                                                                      current_endpoint_index)
        if not self._is_entering_to_session_allowed(current_position, current_endpoint_restrictions, next_position,
                                                    next_endpoint_restrictions):
            raise CannotEnterSession()

        _, next_session_restrictions, _ = self._get_session_info(next_position, next_session_name)

        recorded_args = {}
        for arg_key in next_session_restrictions[self.SESSION_ALLOWED_STORAGE_KEY]:
            if arg_key not in args:
                raise ArgKeyNotPresent(arg_key)
            recorded_args[arg_key] = args[arg_key]

        self._stack_session.push_session(next_session_index)
        self._stack_session.set_arguments_for_current_session(recorded_args)
        self._stack_session.store_in_current_session(self.SESSION_STORAGE_ENDPOINT_KEY, next_endpoint_index)

    def exit_session(self, return_values, is_error=False, error=None):
        if is_error and (error is None):
            raise InvalidArguments('if is_error is True, then error must not be None.')

        current_position, current_session_index, current_endpoint_index = self._get_current_endpoint_index()
        if current_position is None:
            raise NoWorkFlowSessionEntered()

        _, current_session_restrictions, _ = self._get_session_info(current_position, current_session_index)
        allowed_return_values = current_session_restrictions[self.SESSION_ALLOWED_RETURN_VALUES_KEY]

        recorded_return_values = {}
        for return_value_key in allowed_return_values:
            if return_value_key not in return_values:
                raise ReturnArgKeyNotPresent(return_value_key)
            recorded_return_values[return_value_key] = return_values[return_value_key]

        previous_position = self._stack_session.pop_session()
        if previous_position == -1:
            return

        previous_session_index = self._stack_session.get_current_session_id()
        previous_session_return_endpoint_index = self._get_return_endpoint_index_in_session(previous_position,
                                                                                            previous_session_index)
        self._stack_session.store_in_current_session(self.SESSION_STORAGE_ENDPOINT_KEY,
                                                     previous_session_return_endpoint_index)

        if is_error:
            self._stack_session.store_in_current_session(self.SESSION_STORAGE_ERROR_RETURN_VALUE_KEY, error)
        else:
            for recorded_return_value_key in recorded_return_values:
                self._stack_session.store_in_current_session(recorded_return_value_key,
                                                             recorded_return_values[recorded_return_value_key])

    def _is_entering_to_session_allowed(self, current_position, current_endpoint_restrictions, next_position,
                                        next_endpoint_restriction):

        if current_position is None:
            if next_position != 0:
                return False
        else:
            if next_position != current_position + 1:
                return False

        if current_endpoint_restrictions[self.SESSION_ENDPOINT_RESTRICTION_DEAD_END_KEY]:
            return False

        if current_position is not None:
            if not current_endpoint_restrictions[self.SESSION_ENDPOINT_RESTRICTION_CALL_POINT_KEY]:
                return False

        if not next_endpoint_restriction[self.SESSION_ENDPOINT_RESTRICTION_ENTRY_POINT_KEY]:
            return False

        return True

    def _get_return_endpoint_index_in_session(self, position, session_index):
        _, _, endpoints = self._get_session_info(position, session_index)
        for i in range(0, len(endpoints)):
            if endpoints[i][self.SESSION_ENDPOINT_RESTRICTION_KEY][self.SESSION_ENDPOINT_RESTRICTION_RETURN_POINT_KEY]:
                return i
        raise InvalidArguments('No return point in this session')

    def _is_entering_to_endpoint_allowed(self, current_endpoint_index, current_endpoint_restrictions,
                                         next_endpoint_index, next_endpoint_restrictions):
        if current_endpoint_restrictions[self.SESSION_ENDPOINT_RESTRICTION_DEAD_END_KEY]:
            return False

        can_go_to = current_endpoint_restrictions.get(self.SESSION_ENDPOINT_RESTRICTION_CAN_GO_TO)
        if can_go_to is not None:
            if next_endpoint_index not in can_go_to:
                return False

        must_come_from = next_endpoint_restrictions.get(self.SESSION_ENDPOINT_RESTRICTION_MUST_COME_FROM)
        if must_come_from is not None:
            if current_endpoint_index not in must_come_from:
                return False

        if next_endpoint_restrictions[self.SESSION_ENDPOINT_RESTRICTION_EXIT_POINT_KEY]:
            return False

        return True


