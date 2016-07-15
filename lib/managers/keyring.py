from lib.managers.base import BaseManager

from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)

from cryptography.hazmat.backends import default_backend

import os

from db.models.key import Key

from utils import get_current_time


class KeyRingManager(BaseManager):

    SALT_LENGTH = 32

    KEY_LENGTH = 32

    IV_LENGTH = 12

    def __init__(self, session, master_key):
        super(KeyRingManager, self).__init__(session)
        self._master_key = master_key

    def get_key(self, keyid):
        instance = self.session.query(Key).filter(Key.id == keyid).one_or_none()
        if instance is None:
            return None
        _, key = self._decrypt_key(instance.salt+instance.key, self._master_key, instance.iv)
        return key

    def generate_and_save_key(self, expiration_delta):
        key = self.generate_key()
        return key, self.save_key(key, expiration_delta)

    def generate_key(self):
        return os.urandom(self.KEY_LENGTH)

    def save_key(self, key, expiration_delta):
        instance = Key()
        instance.created_at = get_current_time()
        instance.expires_at = instance.created_at + expiration_delta

        instance.iv, instance.salt, instance.key = self._encrypt_key(key, self._master_key)
        self.session.add(instance)
        return instance

    def delete_key(self, keyid):
        instance = self.session.query(Key).filter(Key.id == keyid).one_or_none()
        if instance is None:
            return
        self.session.delete(instance)

    def _encrypt_key(self, key, master_key):
        # Generate a random 96-bit IV.
        iv = os.urandom(self.IV_LENGTH)

        encryptor = Cipher(
            algorithms.AES(master_key),
            modes.CBC(iv),
            backend=default_backend()
        ).encryptor()

        salt = os.urandom(self.SALT_LENGTH)
        encryptor.update(salt)

        return iv, salt, encryptor.update(key) + encryptor.finalize()

    def _decrypt_key(self, encrypted_key, master_key, iv):
        decryptor = Cipher(
            algorithms.AES(master_key),
            modes.CBC(iv),
            backend=default_backend()
        ).decryptor()

        decrypted = decryptor.update(encrypted_key) + decryptor.finalize()
        return decrypted[0:self.SALT_LENGTH], decrypted[self.SALT_LENGTH:self.SALT_LENGTH+self.KEY_LENGTH]
