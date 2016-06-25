from sso.lib.cookie.v1.packer import pack, unpack
from sso.lib.cookie.v1.coder import encode, decode
from sso.lib.cookie.v1.cryptor import encrypt, decrypt

import uuid

import hashlib


class Cookie(object):

    # Field order and their respective size
    user_id_length = 16
    provider_id_length = 16
    user_data_pointer_length = 16
    session_id_length = 16
    session_type_length = 1
    mobile_client_id_length = 16
    mobile_client_secret_hash_length = 32
    issued_at_length = 8
    expires_at_length = 8
    impersonation_info_length = 1

    @classmethod
    def _tobin(cls, token):
        bytes_wrote = 0

        bin_token = bytearray(cls.user_id_length+cls.provider_id_length+cls.user_data_pointer_length +
                              cls.session_id_length+cls.session_type_length+cls.mobile_client_id_length +
                              cls.mobile_client_secret_hash_length+cls.issued_at_length+cls.expires_at_length +
                              cls.impersonation_info_length)

        bin_token[bytes_wrote:bytes_wrote + cls.user_id_length] = token.user_id.bytes
        bytes_wrote += cls.user_id_length

        bin_token[bytes_wrote:bytes_wrote + cls.provider_id_length] = token.provider_id.bytes
        bytes_wrote += cls.provider_id_length

        bin_token[bytes_wrote:bytes_wrote + cls.user_data_pointer_length] = token.user_data_pointer.bytes
        bytes_wrote += cls.user_data_pointer_length

        bin_token[bytes_wrote:bytes_wrote + cls.session_id_length] = token.session_id.bytes
        bytes_wrote += cls.session_id_length

        bin_token[bytes_wrote:bytes_wrote + cls.session_type_length] = token.session_type
        bytes_wrote += cls.session_type_length

        bin_token[bytes_wrote:bytes_wrote+cls.mobile_client_id_length] = token.mobile_client_id.bytes
        bytes_wrote += cls.mobile_client_id_length

        bin_token[bytes_wrote:bytes_wrote+cls.mobile_client_secret_hash_length] = token.mobile_client_secret_hash
        bytes_wrote += cls.mobile_client_secret_hash_length

        bin_token[bytes_wrote:bytes_wrote+cls.issued_at_length] = token.issued_at.to_bytes(cls.issued_at_length, 'big')
        bytes_wrote += cls.issued_at_length

        bin_token[bytes_wrote:bytes_wrote+cls.expires_at_length] = \
            token.expires_at.to_bytes(cls.expires_at_length, 'big')
        bytes_wrote += cls.expires_at_length

        bin_token[bytes_wrote:bytes_wrote+cls.impersonation_info_length] = token.impersonation_info
        bytes_wrote += cls.impersonation_info_length

        return bin_token

    @classmethod
    def _parse(cls, plaintext):
        obj = cls()
        bytes_read = 0

        obj.user_id = uuid.UUID(bytes=plaintext[bytes_read:bytes_read+cls.user_id_length])
        bytes_read += cls.user_id_length

        obj.provider_id = uuid.UUID(bytes=plaintext[bytes_read:bytes_read+cls.provider_id_length])
        bytes_read += cls.provider_id_length

        obj.user_data_pointer = uuid.UUID(bytes=plaintext[bytes_read:bytes_read + cls.user_data_pointer_length])
        bytes_read += cls.user_data_pointer_length

        obj.session_id = uuid.UUID(bytes=plaintext[bytes_read:bytes_read+cls.session_id_length])
        bytes_read += cls.session_id_length

        obj.session_type = plaintext[bytes_read:bytes_read + cls.session_type_length]
        bytes_read += cls.session_type_length

        obj.mobile_client_id = uuid.UUID(bytes=plaintext[bytes_read:bytes_read + cls.mobile_client_id_length])
        bytes_read += cls.mobile_client_id_length

        obj.mobile_client_secret_hash = plaintext[bytes_read:bytes_read+cls.mobile_client_secret_hash_length]
        bytes_read += cls.mobile_client_secret_hash_length

        obj.issued_at = int.from_bytes(plaintext[bytes_read:bytes_read+cls.issued_at_length], 'big')
        bytes_read += cls.issued_at_length

        obj.expires_at = int.from_bytes(plaintext[bytes_read:bytes_read+cls.expires_at_length], 'big')
        bytes_read += cls.expires_at_length

        obj.impersonation_info = plaintext[bytes_read:bytes_read+cls.impersonation_info_length]
        bytes_read += cls.impersonation_info_length

        return obj

    @classmethod
    def deserialize(cls, s, key_retrieval_func):
        binary_data = decode(s)
        iv, tag, keyid_bytes, aad, ciphertext, _ = unpack(binary_data)
        keyid = uuid.UUID(bytes=keyid_bytes)
        key = key_retrieval_func(keyid)
        plaintext = decrypt(key, aad, iv, ciphertext, tag)
        return cls._parse(plaintext)

    @classmethod
    def serialize(cls, token, keyid, key_retrieval_func):
        key = key_retrieval_func(keyid)
        plaintext = cls._tobin(token)
        iv, ciphertext, tag = encrypt(key, plaintext, None)
        packed = pack(iv, ciphertext, tag, None, keyid.bytes)
        return encode(packed)

    @classmethod
    def generate_mobile_client_secret_hash(cls, secret):
        sha = hashlib.sha256()
        sha.update(secret.encode(encoding='utf-8', errors='strict'))
        return sha.digest()

    def __init__(self):
        self._user_id = None
        self._provider_id = None
        self._user_data_pointer = None
        self._session_id = None
        self._session_type = None
        self._mobile_client_id = None
        self._mobile_client_secret_hash = None
        self._impersonation_info = None
        self._issued_at = None
        self._expires_at = None
        self._issued_at = None
        self._impersonation_info = None

    # User id getter and setter
    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, uid):
        self._user_id = uid

    @property
    def provider_id(self):
        return self._provider_id

    @provider_id.setter
    def provider_id(self, pid):
        self._provider_id = pid

    @property
    def user_data_pointer(self):
        return self._user_data_pointer

    @user_data_pointer.setter
    def user_data_pointer(self, pointer):
        self._user_data_pointer = pointer

    # session id getter and setter
    @property
    def session_id(self):
        return self._session_id

    @session_id.setter
    def session_id(self, sid):
        self._session_id = sid

    # Token type getter and setter
    @property
    def session_type(self):
        return self._session_type

    @session_type.setter
    def session_type(self, stp):
        self._session_type = stp

    # Mobile Client id getter and setter
    @property
    def mobile_client_id(self):
        return self._mobile_client_id

    @mobile_client_id.setter
    def mobile_client_id(self, client_id):
        self._mobile_client_id = client_id

    # Mobile Client secret hash getter and setter
    @property
    def mobile_client_secret_hash(self):
        return self._mobile_client_secret_hash

    @mobile_client_secret_hash.setter
    def mobile_client_secret_hash(self, h):
        self._mobile_client_secret_hash = h

    # is impersonated getter and setter
    @property
    def impersonation_info(self):
        return self._impersonation_info

    @impersonation_info.setter
    def impersonation_info(self, info):
        self._impersonation_info = info

    # issued at getter and setter
    @property
    def issued_at(self):
        return self._issued_at

    @issued_at.setter
    def issued_at(self, iat):
        self._issued_at = iat

    # Expires at getter and setter
    @property
    def expires_at(self):
        return self._expires_at

    @expires_at.setter
    def expires_at(self, eat):
        self._expires_at = eat





