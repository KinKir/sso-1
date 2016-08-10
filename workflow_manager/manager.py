OAUTH2_WORKFLOW = {
    'id': 'oauth2',
    'sessions': [
        {
            'name': 'oauth2',
            'global_before_func': None,
            'global_after_func': None,
            'session': {
                'allowed_argument_keys': [],
                'allowed_return_value_keys': [],
                'allowed_storage_keys': []
            },
            'endpoints': [
                {
                    'name': 'auth',
                    'handle_funcs': {
                        'before': None,
                        'after': None
                    },
                    'restrictions': {
                        'entry_point': True,
                        'exit_point': False,
                        'return_point': False,
                        'call_point': True,
                        'direct_access_allowed': True,
                        'allowed_storage_keys': []
                    }
                },
                {
                    'name': 'submit',
                    'handle_funcs': {
                        'before': None,
                        'after': None,
                        'exec': None,
                        'validation': None
                    },
                    'restrictions': {
                        'entry_point': False,
                        'exit_point': True,
                        'return_point': True,
                        'call_point': False,
                        'direct_access_allowed': False,
                        'allowed_storage_keys': []
                    }
                }
            ]
        },
        {
            'name': 'sso',
            'global_before_func': None,
            'global_after_func': None,
            'session': {
                'allowed_argument_keys': [],
                'allowed_return_value_keys': [],
                'allowed_storage_keys': []
            },
            'endpoints': [
                {
                    'name': 'login',
                    'handle_funcs': {
                        'before': None,
                        'after': None
                    },
                    'restrictions': {
                        'entry_point': True,
                        'exit_point': False,
                        'return_point': False,
                        'call_point': True,
                        'direct_access_allowed': True,
                        'allowed_storage_keys': []
                    }
                },
                {
                    'name': 'submit',
                    'handle_funcs': {
                        'before': None,
                        'after': None
                    },
                    'restrictions': {
                        'entry_point': False,
                        'exit_point': True,
                        'return_point': True,
                        'call_point': False,
                        'direct_access_allowed': False,
                        'allowed_storage_keys': []
                    }
                }
            ]
        },
        {
            'name': 'provider',
            'global_before_func': None,
            'global_after_func': None,
            'session': {
                'allowed_argument_keys': [],
                'allowed_storage_keys': [],
                'allowed_return_value_keys': []
            },
            'endpoints_new': [
                {
                    'name': 'choose_provider',
                    'handler_funcs': {
                        'before': None,
                        'after': None
                    },
                    'restrictions': {
                        'entry_point': True,
                        'exit_point': False,
                        'return_point': False,
                        'call_point': False,
                        'direct_access_allowed': True,
                        'can_go_to': [1, 2],
                        'allowed_storage_keys': []
                    }
                },
                {
                    'name': 'choose_social_provider',
                    'handler_funcs': {
                        'before': None,
                        'after': None
                    },
                    'restrictions': {
                        'entry_point': False,
                        'exit_point': False,
                        'return_point': False,
                        'call_point': True,
                        'must_arrive_from': [0],
                        'direct_access_allowed': True,
                        'allowed_storage_keys': []
                    }
                },
                {
                    'name': 'choose_enterprise_tenant',
                    'handler_funcs': {
                        'before': None,
                        'after': None
                    },
                    'restrictions': {
                        'entry_point': False,
                        'exit_point': False,
                        'return_point': False,
                        'call_point': False,
                        'can_go_to': [3],
                        'must_arrive_from': [0],
                        'direct_access_allowed': True,
                        'allowed_storage_keys': []
                    }
                },
                {
                    'name': 'choose_enterprise_provider',
                    'handler_funcs': {
                        'before': None,
                        'after': None
                    },
                    'restrictions': {
                        'entry_point': False,
                        'exit_point': False,
                        'return_point': False,
                        'call_point': True,
                        'must_arrive_from': [0, 2],
                        'direct_access_allowed': False,
                        'allowed_storage_keys': []
                    }
                },
                {
                    'name': 'submit',
                    'handler_funcs': {
                        'before': None,
                        'after': None
                    },
                    'restrictions': {
                        'entry_point': False,
                        'exit_point': True,
                        'return_point': True,
                        'call_point': False,
                        'direct_access_allowed': False,
                        'allowed_storage_keys': []
                    }
                }
            ]
        },
        {
            'name': 'provider_instance',
            'global_before_func': None,
            'global_after_func': None,
            'session': {
                'allowed_argument_keys': [],
                'allowed_storage_keys': [],
                'allowed_return_value_keys': []
            }
        }
    ]
}


class WorkflowManager(object):
    pass
