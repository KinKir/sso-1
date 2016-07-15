from lib.auth_session.v1.packer import pack, unpack
from lib.auth_session.v1.coder import encode, decode
from lib.auth_session.v1.cryptor import encrypt, decrypt

import uuid

import hashlib

AUTH_SESSION_IMPERSONATION_IS_IMPERSONATED = 2

AUTH_SESSION_TYPE_INVALID = 0

AUTH_SESSION_TYPE_WEB = 1

# Stages of session
AUTH_SESSION_STAGE_NOT_INITIALIZED = 0

AUTH_SESSION_STAGE_LOGIN_STARTED = 1

AUTH_SESSION_STAGE_PROVIDER_CHOOSE = 2

AUTH_SESSION_STAGE_PROVIDER_EXECUTION = 3

AUTH_SESSION_STAGE_LOGGED_IN = 4


class Cookie(object):

    # Field order and their respective size
    tenant_id_length = 16
    user_id_length = 16
    provider_id_length = 16
    user_data_pointer_length = 16
    auth_session_id_length = 16
    auth_session_type_length = 1
    auth_session_stage_length = 1
    client_id_length = 16
    client_secret_hash_length = 64
    issued_at_length = 8
    expires_at_length = 8
    logout_token_length = 32
    impersonation_info_length = 1

    @classmethod
    def _tobin(cls, cookie):
        bytes_wrote = 0

        bin_cookie = bytearray(cls.tenant_id_length + cls.user_id_length+cls.provider_id_length +
                               cls.user_data_pointer_length + cls.auth_session_id_length +
                               cls.auth_session_type_length + cls.auth_session_stage_length + cls.client_id_length +
                               cls.client_secret_hash_length + cls.issued_at_length + cls.expires_at_length +
                               cls.logout_token_length + cls.impersonation_info_length)

        bin_cookie[bytes_wrote:bytes_wrote + cls.tenant_id_length] = cookie.tenant_id.bytes
        bytes_wrote += cls.tenant_id_length

        bin_cookie[bytes_wrote:bytes_wrote + cls.user_id_length] = cookie.user_id.bytes
        bytes_wrote += cls.user_id_length

        bin_cookie[bytes_wrote:bytes_wrote + cls.provider_id_length] = cookie.provider_id.bytes
        bytes_wrote += cls.provider_id_length

        bin_cookie[bytes_wrote:bytes_wrote + cls.user_data_pointer_length] = cookie.user_data_pointer.bytes
        bytes_wrote += cls.user_data_pointer_length

        bin_cookie[bytes_wrote:bytes_wrote + cls.auth_session_id_length] = cookie.auth_session_id.bytes
        bytes_wrote += cls.auth_session_id_length

        bin_cookie[bytes_wrote:bytes_wrote + cls.auth_session_type_length] = \
            cookie.auth_session_type.to_bytes(1, byteorder='big')
        bytes_wrote += cls.auth_session_type_length

        bin_cookie[bytes_wrote:bytes_wrote + cls.auth_session_stage_length] = \
            cookie.auth_session_stage.to_bytes(1, byteorder='big')
        bytes_wrote += cls.auth_session_stage_length

        bin_cookie[bytes_wrote:bytes_wrote + cls.client_id_length] = cookie.client_id.bytes
        bytes_wrote += cls.client_id_length

        bin_cookie[bytes_wrote:bytes_wrote + cls.client_secret_hash_length] = cookie.client_secret_hash
        bytes_wrote += cls.client_secret_hash_length

        bin_cookie[bytes_wrote:bytes_wrote+cls.issued_at_length] = \
            cookie.issued_at.to_bytes(cls.issued_at_length, 'big')
        bytes_wrote += cls.issued_at_length

        bin_cookie[bytes_wrote:bytes_wrote+cls.expires_at_length] = \
            cookie.expires_at.to_bytes(cls.expires_at_length, 'big')
        bytes_wrote += cls.expires_at_length

        bin_cookie[bytes_wrote:bytes_wrote + cls.logout_token_length] = cookie.logout_token
        bytes_wrote += cls.logout_token_length

        bin_cookie[bytes_wrote:bytes_wrote+cls.impersonation_info_length] = \
            cookie.impersonation_info.to_bytes(1, byteorder='big')
        bytes_wrote += cls.impersonation_info_length

        return bin_cookie

    @classmethod
    def _parse(cls, plaintext):
        obj = cls()
        bytes_read = 0

        obj.tenant_id = uuid.UUID(bytes=plaintext[bytes_read:bytes_read+cls.tenant_id_length])
        bytes_read += cls.tenant_id_length

        obj.user_id = uuid.UUID(bytes=plaintext[bytes_read:bytes_read+cls.user_id_length])
        bytes_read += cls.user_id_length

        obj.provider_id = uuid.UUID(bytes=plaintext[bytes_read:bytes_read+cls.provider_id_length])
        bytes_read += cls.provider_id_length

        obj.user_data_pointer = uuid.UUID(bytes=plaintext[bytes_read:bytes_read + cls.user_data_pointer_length])
        bytes_read += cls.user_data_pointer_length

        obj.auth_session_id = uuid.UUID(bytes=plaintext[bytes_read:bytes_read + cls.auth_session_id_length])
        bytes_read += cls.auth_session_id_length

        obj.auth_session_type = int.from_bytes(plaintext[bytes_read:bytes_read + cls.auth_session_type_length], 'big')
        bytes_read += cls.auth_session_type_length

        obj.auth_session_stage = int.from_bytes(plaintext[bytes_read:bytes_read + cls.auth_session_stage_length], 'big')
        bytes_read += cls.auth_session_stage_length

        obj.client_id = uuid.UUID(bytes=plaintext[bytes_read:bytes_read + cls.client_id_length])
        bytes_read += cls.client_id_length

        obj.client_secret_hash = plaintext[bytes_read:bytes_read + cls.client_secret_hash_length]
        bytes_read += cls.client_secret_hash_length

        obj.issued_at = int.from_bytes(plaintext[bytes_read:bytes_read+cls.issued_at_length], 'big')
        bytes_read += cls.issued_at_length

        obj.expires_at = int.from_bytes(plaintext[bytes_read:bytes_read+cls.expires_at_length], 'big')
        bytes_read += cls.expires_at_length

        obj.logout_token = plaintext[bytes_read:bytes_read + cls.logout_token_length]
        bytes_read += cls.logout_token_length

        obj.impersonation_info = int.from_bytes(plaintext[bytes_read:bytes_read+cls.impersonation_info_length], 'big')
        bytes_read += cls.impersonation_info_length

        return obj

    @classmethod
    def get_key_id(cls, s):
        binary_data = decode(s)
        _, _, keyid_bytes, _, _, _ = unpack(binary_data)
        return uuid.UUID(bytes=keyid_bytes)

    @classmethod
    def deserialize(cls, s, key_retrieval_func):
        binary_data = decode(s)
        iv, tag, keyid_bytes, aad, ciphertext, _ = unpack(binary_data)
        keyid = uuid.UUID(bytes=keyid_bytes)
        key = key_retrieval_func(keyid)
        plaintext = decrypt(key, aad, iv, ciphertext, tag)
        return keyid, cls._parse(plaintext)

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

    def __init__(self):
        self._tenant_id = uuid.UUID(hex='0' * 32)
        self._user_id = uuid.UUID(hex='0'*32)
        self._provider_id = uuid.UUID(hex='0'*32)
        self._user_data_pointer = uuid.UUID(hex='0'*32)
        self._auth_session_id = uuid.UUID(hex='0' * 32)
        self._auth_session_type = AUTH_SESSION_TYPE_INVALID
        self._auth_session_stage = AUTH_SESSION_STAGE_NOT_INITIALIZED
        self._client_id = uuid.UUID(hex='0'*32)
        self._client_secret_hash = bytes(64)
        self._impersonation_info = 0
        self._issued_at = 0
        self._expires_at = 0
        self._logout_token = bytes(32)

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
    def auth_session_id(self):
        return self._auth_session_id

    @auth_session_id.setter
    def auth_session_id(self, sid):
        self._auth_session_id = sid

    # Token type getter and setter
    @property
    def auth_session_type(self):
        return self._auth_session_type

    @auth_session_type.setter
    def auth_session_type(self, stp):
        if stp >= 256:
            raise OverflowError
        self._auth_session_type = stp

    @property
    def auth_session_stage(self):
        return self._auth_session_stage

    @auth_session_stage.setter
    def auth_session_stage(self, stg):
        if stg >= 256:
            raise OverflowError
        if stg - self._auth_session_stage > 1:
            raise NotImplementedError
        self._auth_session_stage = stg

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

    # logout token getter and setter
    @property
    def logout_token(self):
        return self._logout_token

    @logout_token.setter
    def logout_token(self, lt):
        self._logout_token = lt

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
        return (self._impersonation_info & AUTH_SESSION_IMPERSONATION_IS_IMPERSONATED) == \
               AUTH_SESSION_IMPERSONATION_IS_IMPERSONATED

    @is_impersonated.setter
    def is_impersonated(self, v):
        if v:
            self._impersonation_info |= AUTH_SESSION_IMPERSONATION_IS_IMPERSONATED
        else:
            self._impersonation_info &= (~AUTH_SESSION_IMPERSONATION_IS_IMPERSONATED)

    @property
    def is_web(self):
        return (self._auth_session_type & AUTH_SESSION_TYPE_WEB) == AUTH_SESSION_TYPE_WEB

    @is_web.setter
    def is_web(self, v):
        if v:
            self._auth_session_type |= AUTH_SESSION_TYPE_WEB
        else:
            self._auth_session_type &= (~AUTH_SESSION_TYPE_WEB)

    def is_initialized(self):
        return self._auth_session_type != AUTH_SESSION_TYPE_INVALID and \
               self._auth_session_stage != AUTH_SESSION_STAGE_NOT_INITIALIZED

    def is_choosing_provider(self):
        return self._auth_session_stage == AUTH_SESSION_STAGE_PROVIDER_CHOOSE

    def is_executing_provider(self):
        return self._auth_session_stage == AUTH_SESSION_STAGE_PROVIDER_EXECUTION

    def is_user_logged_in(self):
        return self._auth_session_stage == AUTH_SESSION_STAGE_LOGGED_IN

    def is_login_started(self):
        return self._auth_session_stage == AUTH_SESSION_STAGE_LOGGED_IN










