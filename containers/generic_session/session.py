import ujson
import uuid
from collections import MutableMapping

from containers.generic_session.cryptor import GenericSessionCryptor as Cryptor
from containers.generic_session.packer import GenericSessionPacker as Packer

from containers.generic_session.coder import GenericSessionCoder as Coder


class GenericSession(MutableMapping):

    def __len__(self):
        return self._dict.__len__()

    def __getitem__(self, key):
        return self._dict.__getitem__(key)

    def __iter__(self):
        return self._dict.__iter__()

    def __setitem__(self, key, value):
        if not isinstance(key, str) and not isinstance(key, int):
            raise NotImplementedError
        return self._dict.__setitem__(key, value)

    def __delitem__(self, key):
        return self._dict.__delitem__(key)

    def __init__(self, dictionary):
        if dictionary is None:
            self._dict = {}
        else:
            self._dict = dictionary

    @property
    def __dict__(self):
        return self._dict

    @classmethod
    def _tobin(cls, session):
        return ujson.dumps(session.__dict__).encode(encoding='utf-8', errors='strict')

    @classmethod
    def _parse(cls, plaintext):
        return cls(ujson.loads(plaintext.decode(encoding='utf-8', errors='strict')))

    @classmethod
    def deserialize(cls, s, key_retrieval_func):
        binary_data = Coder.decode(s)
        iv, tag, keyid_bytes, aad, ciphertext, _ = Packer.unpack(binary_data)
        keyid = uuid.UUID(bytes=keyid_bytes)
        key = key_retrieval_func(keyid)
        plaintext = Cryptor.decrypt(key, aad, iv, ciphertext, tag)
        return keyid, cls._parse(plaintext)

    @classmethod
    def serialize(cls, session, keyid, key_retrieval_func):
        if not isinstance(session, cls):
            # TODO: Raise an error
            pass
        key = key_retrieval_func(keyid)
        plaintext = cls._tobin(session)
        iv, ciphertext, tag = Cryptor.encrypt(key, plaintext, None)
        packed = Packer.pack(iv, ciphertext, tag, None, keyid.bytes)
        return Coder.encode(packed)

