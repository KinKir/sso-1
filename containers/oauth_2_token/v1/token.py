import uuid

from containers.generic_token.coder import GenericTokenCoder as Coder
from containers.generic_token.packer import GenericTokenPacker as Packer

from containers.generic_token.cryptor import GenericTokenCryptor as Cryptor
from containers.oauth_2_token.common import OAuth2TokenInterface


class OAuth2Token(OAuth2TokenInterface):

    TOKEN_TYPE_MOBILE = 1

    TOKEN_TYPE_WEB = 2

    TOKEN_TYPE_REFRESH = 4

    TOKEN_TYPE_TIED_TO_SSO_SESSION = 8

    TOKEN_IMPERSONATION_IS_IMPERSONATED = 2

    # Field order and their respective size
    token_id_length = 16
    refresh_token_session_id_length = 16
    sso_session_id_length = 16
    tenant_id_length = 16
    user_id_length = 16
    client_id_length = 16
    user_session_id_length = 16
    client_secret_hash_length = 64
    issued_at_length = 8
    expires_at_length = 8
    impersonation_info_length = 1
    token_type_length = 1

    @classmethod
    def _tobin(cls, token):
        bytes_wrote = 0

        bin_token = bytearray(cls.token_id_length + cls.refresh_token_session_id_length + cls.sso_session_id_length +
                              cls.tenant_id_length + cls.user_id_length +
                              cls.client_id_length + cls.user_session_id_length +
                              cls.client_secret_hash_length + cls.issued_at_length +
                              cls.expires_at_length + cls.impersonation_info_length + cls.token_type_length)

        bin_token[bytes_wrote:bytes_wrote + cls.token_id_length] = token.token_id.bytes
        bytes_wrote += cls.token_id_length

        bin_token[bytes_wrote:bytes_wrote + cls.refresh_token_session_id_length] = token.refresh_token_session_id.bytes
        bytes_wrote += cls.refresh_token_session_id_length

        bin_token[bytes_wrote:bytes_wrote + cls.sso_session_id_length] = token.sso_session_id.bytes
        bytes_wrote += cls.sso_session_id_length

        bin_token[bytes_wrote:bytes_wrote + cls.tenant_id_length] = token.tenant_id.bytes
        bytes_wrote += cls.tenant_id_length

        bin_token[bytes_wrote:bytes_wrote + cls.user_id_length] = token.user_id.bytes
        bytes_wrote += cls.user_id_length

        bin_token[bytes_wrote:bytes_wrote+cls.client_id_length] = token.client_id.bytes
        bytes_wrote += cls.client_id_length

        bin_token[bytes_wrote:bytes_wrote+cls.user_session_id_length] = token.user_session_id.bytes
        bytes_wrote += cls.user_session_id_length

        bin_token[bytes_wrote:bytes_wrote+cls.client_secret_hash_length] = token.client_secret_hash
        bytes_wrote += cls.client_secret_hash_length

        bin_token[bytes_wrote:bytes_wrote+cls.issued_at_length] = token.issued_at.to_bytes(cls.issued_at_length, 'big')
        bytes_wrote += cls.issued_at_length

        bin_token[bytes_wrote:bytes_wrote+cls.expires_at_length] = \
            token.expires_at.to_bytes(cls.expires_at_length, 'big')
        bytes_wrote += cls.expires_at_length

        bin_token[bytes_wrote:bytes_wrote+cls.impersonation_info_length] = \
            token.impersonation_info.to_bytes(1, byteorder='big')
        bytes_wrote += cls.impersonation_info_length

        bin_token[bytes_wrote:bytes_wrote+cls.token_type_length] = token.token_type.to_bytes(1, byteorder='big')
        bytes_wrote += cls.token_type_length

        return bin_token

    @classmethod
    def _parse(cls, plaintext):
        obj = cls()
        bytes_read = 0

        obj.token_id = uuid.UUID(bytes=plaintext[bytes_read:bytes_read + cls.token_id_length])
        bytes_read += cls.token_id_length

        obj.refresh_token_id = uuid.UUID(bytes=plaintext[bytes_read:bytes_read + cls.refresh_token_session_id_length])
        bytes_read += cls.refresh_token_session_id_length

        obj.sso_session_id = uuid.UUID(bytes=plaintext[bytes_read:bytes_read + cls.sso_session_id_length])
        bytes_read += cls.sso_session_id_length

        obj.tenant_id = uuid.UUID(bytes=plaintext[bytes_read:bytes_read + cls.tenant_id_length])
        bytes_read += cls.tenant_id_length

        obj.user_id = uuid.UUID(bytes=plaintext[bytes_read:bytes_read+cls.user_id_length])
        bytes_read += cls.user_id_length

        obj.client_id = uuid.UUID(bytes=plaintext[bytes_read:bytes_read+cls.client_id_length])
        bytes_read += cls.client_id_length

        obj.user_session_id = uuid.UUID(bytes=plaintext[bytes_read:bytes_read+cls.user_session_id_length])
        bytes_read += cls.user_session_id_length

        obj.client_secret_hash = plaintext[bytes_read:bytes_read+cls.client_secret_hash_length]
        bytes_read += cls.client_secret_hash_length

        obj.issued_at = int.from_bytes(plaintext[bytes_read:bytes_read+cls.issued_at_length], 'big')
        bytes_read += cls.issued_at_length

        obj.expires_at = int.from_bytes(plaintext[bytes_read:bytes_read+cls.expires_at_length], 'big')
        bytes_read += cls.expires_at_length

        obj.impersonation_info = \
            int.from_bytes(plaintext[bytes_read:bytes_read+cls.impersonation_info_length], 'big')
        bytes_read += cls.impersonation_info_length

        obj.token_type = \
            int.from_bytes(plaintext[bytes_read:bytes_read+cls.token_type_length], 'big')
        bytes_read += cls.token_type_length

        return obj

    @classmethod
    def get_key_id(cls, s):
        binary_data = Coder.decode(s)
        _, _, keyid_bytes, _, _, _ = Packer.unpack(binary_data)
        return uuid.UUID(bytes=keyid_bytes)

    @classmethod
    def deserialize(cls, s, key_retrieval_func):
        binary_data = Coder.decode(s)
        iv, tag, keyid_bytes, aad, ciphertext, _ = Packer.unpack(binary_data)
        keyid = uuid.UUID(bytes=keyid_bytes)
        key = key_retrieval_func(keyid)
        plaintext = Cryptor.decrypt(key, aad, iv, ciphertext, tag)
        return keyid, cls._parse(plaintext)

    @classmethod
    def serialize(cls, token, keyid, key_retrieval_func):
        if not isinstance(token, cls):
            # TODO: Raise an error
            pass
        key = key_retrieval_func(keyid)
        plaintext = cls._tobin(token)
        iv, ciphertext, tag = Cryptor.encrypt(key, plaintext, None)
        packed = Packer.pack(iv, ciphertext, tag, None, keyid.bytes)
        return Coder.encode(packed)

    def __init__(self):
        self._token_id = uuid.UUID(hex='0'*32)
        self._refresh_token_session_id = uuid.UUID(hex='0' * 32)
        self._sso_session_id = uuid.UUID(hex='0'*32)
        self._tenant_id = uuid.UUID(hex='0'*32)
        self._user_id = uuid.UUID(hex='0'*32)
        self._client_id = uuid.UUID(hex='0'*32)
        self._user_session_id = uuid.UUID(hex='0'*32)
        self._client_secret_hash = bytes(64)
        self._issued_at = 0
        self._expires_at = 0
        self._impersonation_info = 0
        self._token_type = 0

    # oauth_2_token id getter and setter
    @property
    def token_id(self):
        return self._token_id

    @token_id.setter
    def token_id(self, tid):
        self._token_id = tid

    # refresh oauth_2_token id getter and setter (Only there if this oauth_2_token is refresh oauth_2_token)
    @property
    def refresh_token_session_id(self):
        return self._refresh_token_session_id

    @refresh_token_session_id.setter
    def refresh_token_session_id(self, rid):
        self._refresh_token_session_id = rid

    @property
    def sso_session_id(self):
        return self._sso_session_id

    @sso_session_id.setter
    def sso_session_id(self, aid):
        self._sso_session_id = aid

    # Tenant id getter and setter
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

    # Client id getter and setter
    @property
    def client_id(self):
        return self._client_id

    @client_id.setter
    def client_id(self, cid):
        self._client_id = cid

    # User session id getter and setter
    @property
    def user_session_id(self):
        return self._user_session_id

    @user_session_id.setter
    def user_session_id(self, u_sid):
        self._user_session_id = u_sid

    # Token type getter and setter
    @property
    def token_type(self):
        return self._token_type

    @token_type.setter
    def token_type(self, t):
        if t >= 256:
            raise OverflowError
        self._token_type = t

    # Client secret hash getter and setter
    @property
    def client_secret_hash(self):
        return self._client_secret_hash

    @client_secret_hash.setter
    def client_secret_hash(self, h):
        self._client_secret_hash = h

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
    def is_refresh_token(self):
        return (self._token_type & self.TOKEN_TYPE_REFRESH) == self.TOKEN_TYPE_REFRESH

    @is_refresh_token.setter
    def is_refresh_token(self, v):
        if v:
            self._token_type |= self.TOKEN_TYPE_REFRESH
        else:
            self._token_type &= (~self.TOKEN_TYPE_REFRESH)

    @property
    def is_impersonated(self):
        return (self._impersonation_info & self.TOKEN_IMPERSONATION_IS_IMPERSONATED) == \
               self.TOKEN_IMPERSONATION_IS_IMPERSONATED

    @is_impersonated.setter
    def is_impersonated(self, v):
        if v:
            self._impersonation_info |= self.TOKEN_IMPERSONATION_IS_IMPERSONATED
        else:
            self._impersonation_info &= (~self.TOKEN_IMPERSONATION_IS_IMPERSONATED)

    @property
    def is_web(self):
        return (self._token_type & self.TOKEN_TYPE_WEB) == self.TOKEN_TYPE_WEB

    @is_web.setter
    def is_web(self, v):
        if v:
            self._token_type |= self.TOKEN_TYPE_WEB
        else:
            self._token_type &= (~self.TOKEN_TYPE_WEB)

    @property
    def is_tied_to_sso_session(self):
        return (self._token_type & self.TOKEN_TYPE_TIED_TO_SSO_SESSION) == self.TOKEN_TYPE_TIED_TO_SSO_SESSION

    @is_tied_to_sso_session.setter
    def is_tied_to_sso_session(self, v):
        if v:
            self._token_type |= self.TOKEN_TYPE_TIED_TO_SSO_SESSION
        else:
            self._token_type &= (~self.TOKEN_TYPE_TIED_TO_SSO_SESSION)

    def is_valid(self):
        if self.issued_at == 0 or self.expires_at == 0:
            return False

        if self.token_type & self.TOKEN_TYPE_MOBILE != self.TOKEN_TYPE_MOBILE and \
           self.token_type & self.TOKEN_TYPE_WEB != self.TOKEN_TYPE_WEB:
            return False

        return True

    def to_dict(self):
        return {
            'sso_session_id': self.sso_session_id,
            'tenant_id': self.tenant_id,
            'token_id': self.token_id,
            'refresh_token_session_id': self.refresh_token_session_id,
            'user_id': self.user_id,
            'client_id': self.client_id,

            'user_session_id': self.user_session_id,

            'token_type': self.token_type,
            'client_secret_hash': self.client_secret_hash,

            'impersonation_info': self.impersonation_info,
            'issued_at': self.issued_at,
            'expired_at': self.expires_at,

            'is_valid': self.is_valid()

        }
