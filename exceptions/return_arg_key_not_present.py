from exceptions.key_not_present import KeyNotPresent


class ReturnArgKeyNotPresent(KeyNotPresent):
    def __init__(self, key):
        super(ReturnArgKeyNotPresent, self).__init__('Return Value', key)
