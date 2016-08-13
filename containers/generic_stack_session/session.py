import ujson
import uuid

from containers.generic_session.session import GenericSession
from exceptions import UnableToDeserialize
from exceptions import UnableToSerialize
from exceptions import InvalidArguments

from containers.generic_session.coder import Coder
from containers.generic_session.cryptor import Cryptor
from containers.generic_session.packer import Packer


class GenericStackSession(GenericSession):

    STACK_ARCHIVE_KEY = 'a'

    STACK_CURRENT_POSITION_KEY = 'p'

    STACK_ID_KEY = 'i'

    STACK_STORAGE_KEY = 's'

    SESSION_ID_KEY = 'i'

    SESSION_STORAGE_KEY = 's'

    SESSION_ARGUMENTS_KEY = 'a'

    def __init__(self, stack_id, dictionary=None):
        if dictionary is None:
            super(GenericStackSession, self).__init__({})
            self[self.STACK_ARCHIVE_KEY] = {}
            self[self.STACK_STORAGE_KEY] = {}
            self[self.STACK_ID_KEY] = stack_id
            self[self.STACK_CURRENT_POSITION_KEY] = -1
        else:
            super(GenericStackSession, self).__init__(dictionary)
            if self.get(self.STACK_ARCHIVE_KEY) is None:
                raise UnableToDeserialize()
            if self.get(self.STACK_STORAGE_KEY) is None:
                raise UnableToDeserialize()
            if self.get(self.STACK_ID_KEY) is None:
                raise UnableToDeserialize()
            if self.get(self.STACK_CURRENT_POSITION_KEY) is None:
                raise UnableToDeserialize()

    def push_session(self, sid):
        if sid is None:
            raise InvalidArguments()
        current_position = self[self.STACK_CURRENT_POSITION_KEY]
        self[self.STACK_STORAGE_KEY][str(current_position + 1)] = {
            self.SESSION_ARGUMENTS_KEY: {},
            self.SESSION_ID_KEY: sid,
            self.SESSION_STORAGE_KEY: {}
        }
        self[self.STACK_CURRENT_POSITION_KEY] += 1
        return self[self.STACK_CURRENT_POSITION_KEY]

    def pop_session(self):
        current_position = self[self.STACK_CURRENT_POSITION_KEY]
        if current_position == -1:
            raise OverflowError()
        self[self.STACK_ARCHIVE_KEY][str(current_position)] = self[self.STACK_STORAGE_KEY][str(current_position)]
        del self[self.STACK_STORAGE_KEY][str(current_position)]
        self[self.STACK_CURRENT_POSITION_KEY] -= 1
        return self.STACK_CURRENT_POSITION_KEY

    def _get_current_session(self):
        current_position = self[self.STACK_CURRENT_POSITION_KEY]
        if current_position == -1:
            return None
        return self[self.STACK_STORAGE_KEY][str(current_position)]

    def _get_archived_session(self, position):
        archived_session = self[self.STACK_ARCHIVE_KEY].get(str(position))
        return archived_session

    def get_current_session_id(self):
        current_session = self._get_current_session()
        if current_session is None:
            return None
        return current_session[self.SESSION_ID_KEY]

    def get_current_session_storage(self):
        current_session = self._get_current_session()
        if current_session is None:
            return None

        storage_container = {}
        for key in current_session[self.SESSION_STORAGE_KEY]:
            storage_container[key] = current_session[self.SESSION_STORAGE_KEY][key]
        return storage_container

    def get_current_session_storage_value(self, key):
        current_session = self._get_current_session()
        if current_session is None:
            return None
        return current_session[self.SESSION_STORAGE_KEY].get(key)

    def get_current_session_arguments(self):
        current_session = self._get_current_session()
        if current_session is None:
            return None

        arg_container = {}
        for key in current_session[self.SESSION_ARGUMENTS_KEY]:
            arg_container[key] = current_session[self.SESSION_ARGUMENTS_KEY][key]
        return arg_container

    def store_in_current_session(self, key, value):
        session = self._get_current_session()
        if session is None:
            return None
        session[self.SESSION_STORAGE_KEY][key] = value

    def delete_value_in_current_session(self, key):
        session = self._get_current_session()
        if session is None:
            return None
        if session[self.SESSION_STORAGE_KEY].get(key) is None:
            return False
        del session[self.SESSION_STORAGE_KEY][key]
        return True

    def set_arguments_for_current_session(self, args):
        session = self._get_current_session()
        if session is None:
            return None
        for arg_key in args:
            session[self.SESSION_ARGUMENTS_KEY][arg_key] = args[arg_key]

    def get_archived_session_storage(self, position):
        archived_session = self._get_archived_session(position)
        if archived_session is None:
            return None

        storage_container = {}
        for key in archived_session[self.SESSION_STORAGE_KEY]:
            storage_container[key] = archived_session[self.SESSION_STORAGE_KEY][key]
        return storage_container

    def get_archived_session_arguments(self, position):
        archived_session = self._get_archived_session(position)
        if archived_session is None:
            return None

        arg_container = {}
        for key in archived_session[self.SESSION_ARGUMENTS_KEY]:
            arg_container[key] = archived_session[self.SESSION_ARGUMENTS_KEY][key]
        return arg_container

    @property
    def stack_current_position(self):
        return self[self.STACK_CURRENT_POSITION_KEY]

    @property
    def stack_id(self):
        return self[self.STACK_ID_KEY]

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
            raise UnableToSerialize('%s is not an instance of %s' % (session, cls))

        key = key_retrieval_func(keyid)
        plaintext = cls._tobin(session)
        iv, ciphertext, tag = Cryptor.encrypt(key, plaintext, None)
        packed = Packer.pack(iv, ciphertext, tag, None, keyid.bytes)
        return Coder.encode(packed)
