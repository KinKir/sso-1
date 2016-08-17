from exceptions import NoWorkFlowSessionEntered
from exceptions import InvalidWorkflowTemplate
from exceptions import ReturnArgKeyNotPresent
from exceptions import ArgKeyNotPresent
from exceptions import StorageKeyNotAllowed
from exceptions import CannotEnterSession
from exceptions import InvalidArguments
from exceptions import CannotEnterEndpoint
from exceptions import CannotExitSession


class GenericWorkflowStackSession(object):

    SESSION_NAME_KEY = 'name'

    SESSION_RESTRICTIONS_KEY = 'restrictions'

    SESSION_ALLOWED_ARGS_KEY = 'allowed_argument_keys'

    SESSION_ALLOWED_STORAGE_KEY = 'allowed_storage_keys'

    SESSION_ALLOWED_RETURN_VALUES_KEY = 'allowed_return_value_keys'

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

    SESSION_ENDPOINT_RESTRICTION_MUST_COME_FROM = 'must_arrive_from'

    SESSION_ENDPOINT_RESTRICTION_CAN_GO_TO = 'can_go_to'

    SESSION_ERROR_RETURN_VALUE_KEY = 'r_e'

    SESSION_INDEX_KEY = 'index'

    SESSION_INDEX_ENDPOINT_INDEX_KEY = 'index'

    SESSION_INDEX_ENDPOINT_KEY = 'endpoints'

    SESSION_STORAGE_ENDPOINT_KEY = 'e'

    def __init__(self, stack_session_instance, workflow_template):
        if stack_session_instance is None:
            raise InvalidArguments('Stack session instance is None.')
        self._stack_session = stack_session_instance
        is_valid, error_str = self._is_workflow_template_valid(workflow_template)
        if not is_valid:
            raise InvalidWorkflowTemplate(error_str)
        self._workflow_template = workflow_template
        self._session_index = self._index_sessions(workflow_template)

    def _is_workflow_template_valid(self, workflow_template):
        current_position = 0
        current_session = 0

        if len(workflow_template) == 0:
            return False, 'Workflow template cannot be empty array'

        for i in range(0, len(workflow_template)):
            if len(workflow_template[i]) == 0:
                return False, 'Position %d contains empty array' % i

        for position in workflow_template:

            for session in position:
                if self.SESSION_NAME_KEY not in session:
                    return False, 'Session name does not exists for position: %d and session: %d ' % \
                           (current_position, current_session)

                if self.SESSION_RESTRICTIONS_KEY not in session:
                    return False, 'Session restrictions does not exists for position: %d and session: %d' % \
                           (current_position, current_session)

                session_restrictions = session[self.SESSION_RESTRICTIONS_KEY]

                if self.SESSION_ALLOWED_ARGS_KEY not in session_restrictions:
                    return False, 'Session allowed argument key does not exists for position: %d and session: %d ' % \
                           (current_position, current_session)
                if self.SESSION_ALLOWED_RETURN_VALUES_KEY not in session_restrictions:
                    return False, 'Session allowed return keys key does not exists for position: %d ' \
                                  'and session: %d ' % (current_position, current_session)
                if self.SESSION_ALLOWED_STORAGE_KEY not in session_restrictions:
                    return False, 'Session allowed storage keys key does not exists for position: %d ' \
                                  'and session: %d ' % (current_position, current_session)

                if self.SESSION_ERROR_RETURN_VALUE_KEY in \
                   session_restrictions[self.SESSION_ALLOWED_RETURN_VALUES_KEY]:
                    return False, 'Session allowed return keys have reserved key of error for position: %d ' \
                                  'and session: %d ' % (current_position, current_session)

                if self.SESSION_STORAGE_ENDPOINT_KEY in session_restrictions[self.SESSION_ALLOWED_STORAGE_KEY]:
                    return False, 'Session allowed storage keys have reserved key of endpoint for position: %d ' \
                                  'and session: %d ' % (current_position, current_session)
                if self.SESSION_STORAGE_ENDPOINT_KEY in session_restrictions[self.SESSION_ALLOWED_RETURN_VALUES_KEY]:
                    return False, 'Session allowed return value keys have reserved key of endpoint for position: %d ' \
                                  'and session: %d ' % (current_position, current_session)

                if self.SESSION_ENDPOINT_KEY not in session:
                    return False, 'Endpoints are not in session for position: %d ' \
                                  'and session: %d ' % (current_position, current_session)

                endpoints = session[self.SESSION_ENDPOINT_KEY]
                entry_endpoint_exists = False
                exit_endpoint_exists = False

                current_endpoint = 0

                for endpoint in endpoints:
                    if self.SESSION_ENDPOINT_NAME_KEY not in endpoint:
                        return False, 'Endpoint name missing for position: %d, ' \
                                      'session: %d and endpoint: %d' % \
                               (current_position, current_session, current_endpoint)
                    if self.SESSION_ENDPOINT_RESTRICTION_KEY not in endpoint:
                        return False, 'Endpoint restriction missing for position: %d, ' \
                                      'session: %d and endpoint: %d' % \
                               (current_position, current_session, current_endpoint)

                    restriction = endpoint[self.SESSION_ENDPOINT_RESTRICTION_KEY]

                    if self.SESSION_ENDPOINT_RESTRICTION_CALL_POINT_KEY not in restriction:
                        return False, 'Endpoint restriction call point missing for position: %d, ' \
                                      'session: %d and endpoint: %d' % \
                               (current_position, current_session, current_endpoint)
                    if self.SESSION_ENDPOINT_RESTRICTION_ENTRY_POINT_KEY not in restriction:
                        return False, 'Endpoint restriction entry point missing for position: %d, ' \
                                      'session: %d and endpoint: %d' % \
                               (current_position, current_session, current_endpoint)
                    if self.SESSION_ENDPOINT_RESTRICTION_EXIT_POINT_KEY not in restriction:
                        return False, 'Endpoint restriction exit point missing for position: %d, ' \
                                      'session: %d and endpoint: %d' % \
                               (current_position, current_session, current_endpoint)
                    if self.SESSION_ENDPOINT_RESTRICTION_RETURN_POINT_KEY not in restriction:
                        return False, 'Endpoint restriction return point missing for position: %d, ' \
                                      'session: %d and endpoint: %d' % \
                               (current_position, current_session, current_endpoint)
                    if self.SESSION_ENDPOINT_RESTRICTION_DEAD_END_KEY not in restriction:
                        return False, 'Endpoint restriction dead end point missing for position: %d, ' \
                                      'session: %d and endpoint: %d' % \
                               (current_position, current_session, current_endpoint)

                    if restriction[self.SESSION_ENDPOINT_RESTRICTION_ENTRY_POINT_KEY]:
                        entry_endpoint_exists = True
                    if restriction[self.SESSION_ENDPOINT_RESTRICTION_EXIT_POINT_KEY]:
                        exit_endpoint_exists = True

                    current_endpoint += 1

                if not entry_endpoint_exists:
                    return False, 'No endpoint marked as entry point for position: %d, ' \
                                  'session: %d' % \
                           (current_position, current_session)

                if not exit_endpoint_exists:
                    return False, 'No endpoint marked as exit point for position: %d, ' \
                                  'session: %d' % \
                           (current_position, current_session)

                current_session += 1

            current_position += 1

        first_sessions = workflow_template[0]
        for first_session in first_sessions:
            session_restrictions = first_session[self.SESSION_RESTRICTIONS_KEY]
            if len(session_restrictions[self.SESSION_ALLOWED_RETURN_VALUES_KEY]) != 0:
                return False, 'Sessions at first position cannot have allowed return value keys'

        return True, None

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
            return None, None
        return current_position, self._stack_session.get_current_session_id()

    def _get_session_index(self, session_name):
        session_index_node = self._session_index.get(session_name)
        if session_index_node is None:
            return None, None
        return session_index_node[self.SESSION_INDEX_KEY]

    def _get_current_endpoint_index(self):
        current_position, current_index = self._get_current_session_index()
        if current_position is None:
            return None, None, None
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
        if position is None:
            return None, None, None
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
        if position is None:
            return None, None, None
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

        return_values = self._stack_session.get_previous_session_return_values()
        if self.SESSION_ERROR_RETURN_VALUE_KEY in return_values:
            return True, return_values[self.SESSION_ERROR_RETURN_VALUE_KEY]

        return False, return_values

    def remove_previous_session_return_value(self):
        current_position, current_session_index = self._get_current_session_index()
        if current_position is None:
            raise NoWorkFlowSessionEntered()

        self._stack_session.clear_previous_session_return_value()

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
        if next_endpoint_restrictions.get(self.SESSION_ENDPOINT_RESTRICTION_AUTO_ARRIVE_ALLOWED_FROM_KEY) is not None:
            if current_endpoint_index not in \
                   next_endpoint_restrictions.get(self.SESSION_ENDPOINT_RESTRICTION_AUTO_ARRIVE_ALLOWED_FROM_KEY):
                raise CannotEnterEndpoint('Endpoint does not allow auto arrive from current endpoint.')
            if not self._is_entering_to_endpoint_allowed(current_endpoint_index, current_endpoint_restrictions,
                                                         next_endpoint_index, next_endpoint_restrictions):
                raise CannotEnterEndpoint()
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

        _, next_session_restrictions, _ = self._get_session_info(next_position, next_session_index)

        recorded_args = {}
        for arg_key in next_session_restrictions[self.SESSION_ALLOWED_ARGS_KEY]:
            if arg_key not in args:
                raise ArgKeyNotPresent(arg_key)
            recorded_args[arg_key] = args[arg_key]

        self._stack_session.push_session(next_session_index)
        self._stack_session.set_arguments_for_current_session(recorded_args)
        self._stack_session.store_in_current_session(self.SESSION_STORAGE_ENDPOINT_KEY, next_endpoint_index)

    def exit_session(self, return_values, return_endpoint_name, is_error=False, error=None):
        if is_error and (error is None):
            raise InvalidArguments('if is_error is True, then error must not be None.')

        if return_endpoint_name is None:
            raise InvalidArguments('Return endpoint name is compulsory.')

        current_position, current_session_index, current_endpoint_index = self._get_current_endpoint_index()
        if current_position is None:
            raise NoWorkFlowSessionEntered()

        _, _, current_endpoint_restrictions = self._get_endpoint_info(current_position, current_session_index,
                                                                      current_endpoint_index)

        if not current_endpoint_restrictions[self.SESSION_ENDPOINT_RESTRICTION_EXIT_POINT_KEY]:
            raise CannotExitSession('Current endpoint is not marked as exit point')

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
                                                                                            previous_session_index,
                                                                                            return_endpoint_name)
        self._stack_session.store_in_current_session(self.SESSION_STORAGE_ENDPOINT_KEY,
                                                     previous_session_return_endpoint_index)

        if is_error:
            self._stack_session.set_previous_session_return_value({self.SESSION_ERROR_RETURN_VALUE_KEY: error})
        else:
            self._stack_session.set_previous_session_return_value(recorded_return_values)

    def _is_entering_to_session_allowed(self, current_position, current_endpoint_restrictions, next_position,
                                        next_endpoint_restriction):

        if current_position is None:
            if next_position != 0:
                return False
        else:
            if next_position != current_position + 1:
                return False

        if current_position is not None:
            if current_endpoint_restrictions[self.SESSION_ENDPOINT_RESTRICTION_DEAD_END_KEY]:
                return False
            if not current_endpoint_restrictions[self.SESSION_ENDPOINT_RESTRICTION_CALL_POINT_KEY]:
                return False

        if not next_endpoint_restriction[self.SESSION_ENDPOINT_RESTRICTION_ENTRY_POINT_KEY]:
            return False

        return True

    def _get_return_endpoint_index_in_session(self, position, session_index, return_endpoint_name):
        _, _, endpoints = self._get_session_info(position, session_index)

        for i in range(0, len(endpoints)):

            restrictions = endpoints[i][self.SESSION_ENDPOINT_RESTRICTION_KEY]

            if return_endpoint_name is not None:
                if endpoints[i][self.SESSION_ENDPOINT_NAME_KEY] == return_endpoint_name:
                    if restrictions[self.SESSION_ENDPOINT_RESTRICTION_RETURN_POINT_KEY]:
                        return i
                    else:
                        raise InvalidArguments('Preferred endpoint is not marked as return endpoint.')
            else:
                if restrictions[self.SESSION_ENDPOINT_RESTRICTION_RETURN_POINT_KEY]:
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

        return True


