from exceptions.key_not_present import KeyNotPresent


class ArgKeyNotPresent(KeyNotPresent):
    def __init__(self, key):
        super(ArgKeyNotPresent, self).__init__('Argument', key)
