from exceptions.key_not_present import KeyNotPresent


class StorageKeyNotPresent(KeyNotPresent):
    def __init__(self, key):
        super(StorageKeyNotPresent, self).__init__('Storage key', key)
