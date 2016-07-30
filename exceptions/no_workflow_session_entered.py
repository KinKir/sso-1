class NoWorkFlowSessionEntered(Exception):
    # This exception will be raised, when
    # we try to do some operation on instance of,
    # workflow stacked session, but there is no
    # current session.
    pass
