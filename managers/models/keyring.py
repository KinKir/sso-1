import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)

from db.models.key import Key
from managers.base import BaseManager
from utils import get_current_time


class KeyRingManager(BaseManager):

    def __init__(self, session, master_key):
        super(KeyRingManager, self).__init__(session)
        self._master_key = master_key

    def get_key(self, keyid):
        instance = self.session.query(Key).filter(Key.id == keyid).one_or_none()
        if instance is None:
            return None
        _, key = self._decrypt_key(bytes.fromhex(instance.salt)+bytes.fromhex(instance.encrypted_key), self._master_key,
                                   bytes.fromhex(instance.iv))
        return key

    def generate_and_save_key(self, expiration_delta):
        key = self.generate_key()
        return key, self.save_key(key, expiration_delta)

    @staticmethod
    def generate_key():
        return os.urandom(Key.KEY_LENGTH)

    def save_key(self, key, expiration_delta):
        instance = Key()
        instance.created_at = get_current_time()
        instance.expires_at = instance.created_at + expiration_delta

        iv, salt, encrypted_key = self._encrypt_key(key, self._master_key)
        instance.iv = iv.hex()
        instance.salt = salt.hex()
        instance.encrypted_key = iv.hex()

        self.session.add(instance)
        return instance

    def delete_key(self, keyid):
        instance = self.session.query(Key).filter(Key.id == keyid).one_or_none()
        if instance is None:
            return
        self.session.delete(instance)

    @staticmethod
    def _encrypt_key(key, master_key):
        # Generate a random 96-bit IV.
        iv = os.urandom(Key.IV_LENGTH)

        encryptor = Cipher(
            algorithms.AES(master_key),
            modes.CBC(iv),
            backend=default_backend()
        ).encryptor()

        salt = os.urandom(Key.SALT_LENGTH)
        encryptor.update(salt)

        return iv, salt, encryptor.update(key) + encryptor.finalize()

    @staticmethod
    def _decrypt_key(encrypted_key, master_key, iv):
        decryptor = Cipher(
            algorithms.AES(master_key),
            modes.CBC(iv),
            backend=default_backend()
        ).decryptor()

        decrypted = decryptor.update(encrypted_key) + decryptor.finalize()
        return decrypted[0:Key.SALT_LENGTH], decrypted[Key.SALT_LENGTH:Key.SALT_LENGTH+Key.KEY_LENGTH]
