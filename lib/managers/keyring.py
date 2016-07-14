from lib.managers.base import Manager


class KeyRingManager(Manager):
    def __init__(self, session, master_key):
        super(KeyRingManager, self).__init__(session)
        self._master_key = master_key

    def get_key(self, keyid):
        pass

    def generate_key(self, expires_at):
        pass

    def delete_key(self, keyid):
        pass
