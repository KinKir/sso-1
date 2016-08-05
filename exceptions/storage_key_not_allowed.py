from exceptions.key_not_present import KeyNotPresent


class StorageKeyNotAllowed(KeyNotPresent):
    def __init__(self, key):
        super(StorageKeyNotAllowed, self).__init__('Storage key', key)
