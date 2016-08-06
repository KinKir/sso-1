import ujson
import uuid

from containers.generic_session.session import GenericSession
from exceptions import UnableToSerializeData

from containers.generic_session.coder import Coder
from containers.generic_session.cryptor import Cryptor
from containers.generic_session.packer import Packer


class GenericStackSession(GenericSession):

    STORAGE_KEY = 'd'

    ARCHIVE_KEY = 'e'

    ID_KEY = 'i'

    NEXT_SID_KEY = 'n'

    def __init__(self, stack_id, dictionary=None):
        if dictionary is None:
            super(GenericStackSession, self).__init__({})
            self[self.STORAGE_KEY] = {}
            self[self.ARCHIVE_KEY] = {}
            self[self.ID_KEY] = stack_id
            self[self.NEXT_SID_KEY] = 0
        else:
            super(GenericStackSession, self).__init__(dictionary)
            if self.get(self.NEXT_SID_KEY) is None:
                raise UnableToSerializeData()
            if self.get(self.STORAGE_KEY) is None:
                raise UnableToSerializeData()
            if self.get(self.ARCHIVE_KEY) is None:
                raise UnableToSerializeData()
            if self.get(self.ID_KEY) is None:
                raise UnableToSerializeData()

    def push_session(self):
        current_sid = self[self.NEXT_SID_KEY]
        self[self.STORAGE_KEY][str(current_sid)] = {}
        self[self.NEXT_SID_KEY] += 1
        return self[self.NEXT_SID_KEY], current_sid, self[self.STORAGE_KEY][str(current_sid)]

    def pop_session(self):
        if self[self.NEXT_SID_KEY] == 0:
            raise OverflowError

        current_sid = self[self.NEXT_SID_KEY] - 1
        self[self.ARCHIVE_KEY][str(current_sid)] = self[self.STORAGE_KEY][str(current_sid)]

        del self[self.STORAGE_KEY][str(current_sid)]
        self[self.NEXT_SID_KEY] -= 1
        return self[self.NEXT_SID_KEY]

    def get_current_session(self):
        current_sid = self[self.NEXT_SID_KEY] - 1
        if current_sid == -1:
            return -1, None
        return current_sid, self[self.STORAGE_KEY][str(current_sid)]

    def store_in_current_session(self, key, value):
        _, current_session = self.get_current_session()
        current_session[key] = value

    def get_session(self, sid):
        return self[self.STORAGE_KEY].get(str(sid))

    def get_max_sid_issued(self):
        return self[self.NEXT_SID_KEY] - 1

    def get_archived_sessions(self):
        return self[self.ARCHIVE_KEY]

    @classmethod
    def _tobin(cls, session):
        return ujson.dumps(session.__dict__).encode(encoding='utf-8', errors='strict')

    @classmethod
    def _parse(cls, plaintext):
        return cls(None, ujson.loads(plaintext.decode(encoding='utf-8', errors='strict')))

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
