class KeyNotPresent(Exception):
    def __init__(self, key_type, key):
        super(KeyNotPresent, self).__init__('%s Key: %s is not present or allowed' % (key_type, key))
        self.key = key

