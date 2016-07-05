from lib.cookie.v1.packer import pack, unpack
from lib.cookie.v1.coder import encode, decode
from lib.cookie.v1.cryptor import encrypt, decrypt

import uuid

import hashlib

SESSION_IMPERSONATION_IS_IMPERSONATED = 2

SESSION_TYPE_MOBILE = 1

SESSION_TYPE_WEB = 2


class Cookie(object):

    # Field order and their respective size
    tenant_id_length = 16
    user_id_length = 16
    provider_id_length = 16
    user_data_pointer_length = 16
    oauth_params_pointer_length = 16
    session_id_length = 16
    session_type_length = 1
    client_id_length = 16
    client_secret_hash_length = 32
    mobile_client_id_length = 16
    mobile_client_secret_hash_length = 32
    issued_at_length = 8
    expires_at_length = 8
    impersonation_info_length = 1

    @classmethod
    def _tobin(cls, token):
        bytes_wrote = 0

        bin_token = bytearray(cls.tenant_id_length+cls.user_id_length+cls.provider_id_length +
                              cls.user_data_pointer_length+cls.session_id_length+cls.session_type_length +
                              cls.client_id_length+cls.client_secret_hash_length+cls.mobile_client_id_length +
                              cls.mobile_client_secret_hash_length+cls.issued_at_length+cls.expires_at_length +
                              cls.impersonation_info_length)

        bin_token[bytes_wrote:bytes_wrote + cls.tenant_id_length] = token.tenant_id.bytes
        bytes_wrote += cls.tenant_id_length

        bin_token[bytes_wrote:bytes_wrote + cls.user_id_length] = token.user_id.bytes
        bytes_wrote += cls.user_id_length

        bin_token[bytes_wrote:bytes_wrote + cls.provider_id_length] = token.provider_id.bytes
        bytes_wrote += cls.provider_id_length

        bin_token[bytes_wrote:bytes_wrote + cls.user_data_pointer_length] = token.user_data_pointer.bytes
        bytes_wrote += cls.user_data_pointer_length

        bin_token[bytes_wrote:bytes_wrote + cls.session_id_length] = token.session_id.bytes
        bytes_wrote += cls.session_id_length

        bin_token[bytes_wrote:bytes_wrote + cls.session_type_length] = token.session_type.to_bytes(1, byteorder='big')
        bytes_wrote += cls.session_type_length

        bin_token[bytes_wrote:bytes_wrote + cls.client_id_length] = token.client_id.bytes
        bytes_wrote += cls.client_id_length

        bin_token[bytes_wrote:bytes_wrote + cls.client_secret_hash_length] = token.client_secret_hash
        bytes_wrote += cls.client_secret_hash_length

        bin_token[bytes_wrote:bytes_wrote+cls.mobile_client_id_length] = token.mobile_client_id.bytes
        bytes_wrote += cls.mobile_client_id_length

        bin_token[bytes_wrote:bytes_wrote+cls.mobile_client_secret_hash_length] = token.mobile_client_secret_hash
        bytes_wrote += cls.mobile_client_secret_hash_length

        bin_token[bytes_wrote:bytes_wrote+cls.issued_at_length] = token.issued_at.to_bytes(cls.issued_at_length, 'big')
        bytes_wrote += cls.issued_at_length

        bin_token[bytes_wrote:bytes_wrote+cls.expires_at_length] = \
            token.expires_at.to_bytes(cls.expires_at_length, 'big')
        bytes_wrote += cls.expires_at_length

        bin_token[bytes_wrote:bytes_wrote+cls.impersonation_info_length] = \
            token.impersonation_info.to_bytes(1, byteorder='big')
        bytes_wrote += cls.impersonation_info_length

        return bin_token

    @classmethod
    def _parse(cls, plaintext):
        obj = cls()
        bytes_read = 0

        obj.tenant_id = uuid.UUID(bytes=plaintext[bytes_read:bytes_read + cls.tenant_id_length])
        bytes_read += cls.tenant_id_length

        obj.user_id = uuid.UUID(bytes=plaintext[bytes_read:bytes_read+cls.user_id_length])
        bytes_read += cls.user_id_length

        obj.provider_id = uuid.UUID(bytes=plaintext[bytes_read:bytes_read+cls.provider_id_length])
        bytes_read += cls.provider_id_length

        obj.user_data_pointer = uuid.UUID(bytes=plaintext[bytes_read:bytes_read + cls.user_data_pointer_length])
        bytes_read += cls.user_data_pointer_length

        obj.session_id = uuid.UUID(bytes=plaintext[bytes_read:bytes_read+cls.session_id_length])
        bytes_read += cls.session_id_length

        obj.session_type = int.from_bytes(plaintext[bytes_read:bytes_read + cls.session_type_length], 'big')
        bytes_read += cls.session_type_length

        obj.client_id = uuid.UUID(bytes=plaintext[bytes_read:bytes_read + cls.client_id_length])
        bytes_read += cls.client_id_length

        obj.client_secret_hash = plaintext[bytes_read:bytes_read + cls.client_secret_hash_length]
        bytes_read += cls.client_secret_hash_length

        obj.mobile_client_id = uuid.UUID(bytes=plaintext[bytes_read:bytes_read + cls.mobile_client_id_length])
        bytes_read += cls.mobile_client_id_length

        obj.mobile_client_secret_hash = plaintext[bytes_read:bytes_read+cls.mobile_client_secret_hash_length]
        bytes_read += cls.mobile_client_secret_hash_length

        obj.issued_at = int.from_bytes(plaintext[bytes_read:bytes_read+cls.issued_at_length], 'big')
        bytes_read += cls.issued_at_length

        obj.expires_at = int.from_bytes(plaintext[bytes_read:bytes_read+cls.expires_at_length], 'big')
        bytes_read += cls.expires_at_length

        obj.impersonation_info = int.from_bytes(plaintext[bytes_read:bytes_read+cls.impersonation_info_length], 'big')
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
    def serialize(cls, cookie, keyid, key_retrieval_func):
        key = key_retrieval_func(keyid)
        plaintext = cls._tobin(cookie)
        iv, ciphertext, tag = encrypt(key, plaintext, None)
        packed = pack(iv, ciphertext, tag, None, keyid.bytes)
        return encode(packed)

    @classmethod
    def generate_client_secret_hash(cls, secret):
        sha = hashlib.sha256()
        sha.update(secret.encode(encoding='utf-8', errors='strict'))
        return sha.digest()

    @classmethod
    def generate_mobile_client_secret_hash(cls, secret):
        sha = hashlib.sha256()
        sha.update(secret.encode(encoding='utf-8', errors='strict'))
        return sha.digest()

    def __init__(self):
        self._tenant_id = uuid.UUID(hex='0' * 32)
        self._user_id = uuid.UUID(hex='0'*32)
        self._provider_id = uuid.UUID(hex='0'*32)
        self._user_data_pointer = uuid.UUID(hex='0'*32)
        self._session_id = uuid.UUID(hex='0'*32)
        self._session_type = 0
        self._client_id = uuid.UUID(hex='0'*32)
        self._client_secret_hash = bytes(32)
        self._mobile_client_id = uuid.UUID(hex='0'*32)
        self._mobile_client_secret_hash = bytes(32)
        self._impersonation_info = 0
        self._issued_at = 0
        self._expires_at = 0

    @property
    def tenant_id(self):
        return self._tenant_id

    @tenant_id.setter
    def tenant_id(self, tid):
        self._tenant_id = tid

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
        if stp >= 256:
            raise OverflowError
        self._session_type = stp

    # Client id getter and setter
    @property
    def client_id(self):
        return self._client_id

    @client_id.setter
    def client_id(self, cid):
        self._client_id = cid

    # Client secret hash getter and setter
    @property
    def client_secret_hash(self):
        return self._client_secret_hash

    @client_secret_hash.setter
    def client_secret_hash(self, h):
        self._client_secret_hash = h

    # Mobile Client id getter and setter
    @property
    def mobile_client_id(self):
        return self._mobile_client_id

    @mobile_client_id.setter
    def mobile_client_id(self, cid):
        self._mobile_client_id = cid

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
        if info >= 256:
            raise OverflowError
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

    @property
    def is_impersonated(self):
        return (self._impersonation_info & SESSION_IMPERSONATION_IS_IMPERSONATED) == \
               SESSION_IMPERSONATION_IS_IMPERSONATED

    @is_impersonated.setter
    def is_impersonated(self, v):
        if v:
            self._impersonation_info |= SESSION_IMPERSONATION_IS_IMPERSONATED
        else:
            self._impersonation_info &= (~SESSION_IMPERSONATION_IS_IMPERSONATED)

    @property
    def is_mobile(self):
        return (self._session_type & SESSION_TYPE_MOBILE) == SESSION_TYPE_MOBILE

    @is_mobile.setter
    def is_mobile(self, v):
        if v:
            self._session_type |= SESSION_TYPE_MOBILE
        else:
            self._session_type &= (~SESSION_TYPE_MOBILE)

    @property
    def is_web(self):
        return (self._session_type & SESSION_TYPE_WEB) == SESSION_TYPE_WEB

    @is_web.setter
    def is_web(self, v):
        if v:
            self._session_type |= SESSION_TYPE_WEB
        else:
            self._session_type &= (~SESSION_TYPE_WEB)








