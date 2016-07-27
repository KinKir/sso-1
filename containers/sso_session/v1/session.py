import uuid

from containers.generic_session.cryptor import GenericSessionCryptor as Cryptor
from containers.generic_session.packer import GenericSessionPacker as Packer

from containers.generic_session.coder import GenericSessionCoder as Coder
from containers.sso_session.common import SSOSessionInterface


class SSOSession(SSOSessionInterface):
    SSO_SESSION_IMPERSONATION_IS_IMPERSONATED = 2

    SSO_SESSION_TYPE_INVALID = 0

    SSO_SESSION_TYPE_WEB = 1

    SSO_SESSION_TYPE_MOBILE = 2

    # Field order and their respective size
    tenant_id_length = 16
    user_id_length = 16
    provider_id_length = 16
    user_data_pointer_length = 16
    sso_session_id_length = 16
    sso_session_type_length = 1
    sso_session_meta_data_pointer_length = 16
    issued_at_length = 8
    expires_at_length = 8
    logout_token_length = 32
    impersonation_info_length = 1

    @classmethod
    def _tobin(cls, obj):
        bytes_wrote = 0

        bin_obj = bytearray(cls.tenant_id_length + cls.user_id_length + cls.provider_id_length +
                            cls.user_data_pointer_length + cls.sso_session_id_length +
                            cls.sso_session_type_length +
                            cls.sso_session_meta_data_pointer_length +
                            cls.issued_at_length + cls.expires_at_length +
                            cls.logout_token_length + cls.impersonation_info_length)

        bin_obj[bytes_wrote:bytes_wrote + cls.tenant_id_length] = obj.tenant_id.bytes
        bytes_wrote += cls.tenant_id_length

        bin_obj[bytes_wrote:bytes_wrote + cls.user_id_length] = obj.user_id.bytes
        bytes_wrote += cls.user_id_length

        bin_obj[bytes_wrote:bytes_wrote + cls.provider_id_length] = obj.provider_id.bytes
        bytes_wrote += cls.provider_id_length

        bin_obj[bytes_wrote:bytes_wrote + cls.user_data_pointer_length] = obj.user_data_pointer.bytes
        bytes_wrote += cls.user_data_pointer_length

        bin_obj[bytes_wrote:bytes_wrote + cls.sso_session_id_length] = obj.sso_session_id.bytes
        bytes_wrote += cls.sso_session_id_length

        bin_obj[bytes_wrote:bytes_wrote + cls.sso_session_type_length] = \
            obj.sso_session_type.to_bytes(1, byteorder='big')
        bytes_wrote += cls.sso_session_type_length

        bin_obj[bytes_wrote:bytes_wrote + cls.sso_session_meta_data_pointer_length] = \
            obj.sso_session_meta_data_pointer.bytes
        bytes_wrote += cls.sso_session_meta_data_pointer_length

        bin_obj[bytes_wrote:bytes_wrote+cls.issued_at_length] = \
            obj.issued_at.to_bytes(cls.issued_at_length, 'big')
        bytes_wrote += cls.issued_at_length

        bin_obj[bytes_wrote:bytes_wrote+cls.expires_at_length] = \
            obj.expires_at.to_bytes(cls.expires_at_length, 'big')
        bytes_wrote += cls.expires_at_length

        bin_obj[bytes_wrote:bytes_wrote + cls.logout_token_length] = obj.logout_token
        bytes_wrote += cls.logout_token_length

        bin_obj[bytes_wrote:bytes_wrote+cls.impersonation_info_length] = \
            obj.impersonation_info.to_bytes(1, byteorder='big')
        bytes_wrote += cls.impersonation_info_length

        return bin_obj

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

        obj.sso_session_id = uuid.UUID(bytes=plaintext[bytes_read:bytes_read + cls.sso_session_id_length])
        bytes_read += cls.sso_session_id_length

        obj.sso_session_type = int.from_bytes(plaintext[bytes_read:bytes_read + cls.sso_session_type_length], 'big')
        bytes_read += cls.sso_session_type_length

        obj.sso_session_meta_data_pointer = \
            uuid.UUID(bytes=plaintext[bytes_read:bytes_read + cls.sso_session_meta_data_pointer_length])
        bytes_read += cls.sso_session_meta_data_pointer_length

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
    def serialize(cls, obj, keyid, key_retrieval_func):
        if not isinstance(obj, cls):
            # TODO: Raise an error
            pass
        key = key_retrieval_func(keyid)
        plaintext = cls._tobin(obj)
        iv, ciphertext, tag = Cryptor.encrypt(key, plaintext, None)
        packed = Packer.pack(iv, ciphertext, tag, None, keyid.bytes)
        return Coder.encode(packed)

    def __init__(self):
        self._tenant_id = uuid.UUID(hex='0' * 32)
        self._user_id = uuid.UUID(hex='0'*32)
        self._provider_id = uuid.UUID(hex='0'*32)
        self._user_data_pointer = uuid.UUID(hex='0'*32)
        self._sso_session_id = uuid.UUID(hex='0' * 32)
        self._sso_session_type = self.SSO_SESSION_TYPE_INVALID
        self._sso_session_meta_data_pointer = uuid.UUID(hex='0'*32)
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

    # sso session id getter and setter
    @property
    def sso_session_id(self):
        return self._sso_session_id

    @sso_session_id.setter
    def sso_session_id(self, sid):
        self._sso_session_id = sid

    # sso session type getter and setter
    @property
    def sso_session_type(self):
        return self._sso_session_type

    @sso_session_type.setter
    def sso_session_type(self, stp):
        if stp >= 256:
            raise OverflowError
        self._sso_session_type = stp

    @property
    def sso_session_meta_data_pointer(self):
        return self._sso_session_meta_data_pointer

    @sso_session_meta_data_pointer.setter
    def sso_session_meta_data_pointer(self, stg):
        self._sso_session_meta_data_pointer = stg

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
        return (self._impersonation_info & self.SSO_SESSION_IMPERSONATION_IS_IMPERSONATED) == \
               self.SSO_SESSION_IMPERSONATION_IS_IMPERSONATED

    @is_impersonated.setter
    def is_impersonated(self, v):
        if v:
            self._impersonation_info |= self.SSO_SESSION_IMPERSONATION_IS_IMPERSONATED
        else:
            self._impersonation_info &= (~self.SSO_SESSION_IMPERSONATION_IS_IMPERSONATED)

    @property
    def is_web(self):
        return (self._sso_session_type & self.SSO_SESSION_TYPE_WEB) == self.SSO_SESSION_TYPE_WEB

    @is_web.setter
    def is_web(self, v):
        if v:
            self._sso_session_type |= self.SSO_SESSION_TYPE_WEB
        else:
            self._sso_session_type &= (~self.SSO_SESSION_TYPE_WEB)

    @property
    def is_mobile(self):
        return (self._sso_session_type & self.SSO_SESSION_TYPE_MOBILE) == self.SSO_SESSION_TYPE_MOBILE

    @is_mobile.setter
    def is_mobile(self, v):
        if v:
            self._sso_session_type |= self.SSO_SESSION_TYPE_MOBILE
        else:
            self._sso_session_type &= (~self.SSO_SESSION_TYPE_MOBILE)

    def is_valid(self):
        pass

    def to_dict(self):
        return {
            'tenant_id': self.tenant_id,
            'user_id': self.user_id,
            'provider_id': self.provider_id,
            'user_data_pointer': self.user_data_pointer,
            'sso_session_id': self.sso_session_id,
            'sso_session_type': self.sso_session_type,
            'logout_token': self.logout_token,
            'impersonation_info': self.impersonation_info,
            'issued_at': self.issued_at,
            'expires_at': self.expires_at
        }
