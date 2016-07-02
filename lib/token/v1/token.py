from lib.token.common import TokenInterface
from lib.token.v1.packer import pack, unpack
from lib.token.v1.coder import encode, decode
from lib.token.v1.cryptor import encrypt, decrypt

import uuid

import hashlib

TOKEN_TYPE_MOBILE = 1

TOKEN_TYPE_WEB = 2

TOKEN_IMPERSONATION_IS_IMPERSONATED = 1


class Token(TokenInterface):

    # Field order and their respective size
    organization_id_length = 16
    user_id_length = 16
    client_id_length = 16
    mobile_client_id_length = 16
    user_session_id_length = 16
    client_secret_hash_length = 32
    mobile_client_secret_hash_length = 32
    issued_at_length = 8
    expires_at_length = 8
    impersonation_info_length = 1
    token_type_length = 1

    @classmethod
    def _tobin(cls, token):
        bytes_wrote = 0

        bin_token = bytearray(cls.organization_id_length + cls.user_id_length+cls.client_id_length +
                              cls.mobile_client_id_length+cls.user_session_id_length+cls.client_secret_hash_length +
                              cls.mobile_client_secret_hash_length+cls.issued_at_length+cls.expires_at_length +
                              cls.impersonation_info_length+cls.token_type_length)

        bin_token[bytes_wrote:bytes_wrote+cls.organization_id_length] = token.organization_id.bytes
        bytes_wrote += cls.organization_id_length

        bin_token[bytes_wrote:bytes_wrote + cls.user_id_length] = token.user_id.bytes
        bytes_wrote += cls.user_id_length

        bin_token[bytes_wrote:bytes_wrote+cls.client_id_length] = token.client_id.bytes
        bytes_wrote += cls.client_id_length

        bin_token[bytes_wrote:bytes_wrote+cls.mobile_client_id_length] = token.mobile_client_id.bytes
        bytes_wrote += cls.mobile_client_id_length

        bin_token[bytes_wrote:bytes_wrote+cls.user_session_id_length] = token.user_session_id.bytes
        bytes_wrote += cls.user_session_id_length

        bin_token[bytes_wrote:bytes_wrote+cls.client_secret_hash_length] = token.client_secret_hash
        bytes_wrote += cls.client_secret_hash_length

        bin_token[bytes_wrote:bytes_wrote+cls.mobile_client_secret_hash_length] = token.mobile_client_secret_hash
        bytes_wrote += cls.mobile_client_secret_hash_length

        bin_token[bytes_wrote:bytes_wrote+cls.issued_at_length] = token.issued_at.to_bytes(cls.issued_at_length, 'big')
        bytes_wrote += cls.issued_at_length

        bin_token[bytes_wrote:bytes_wrote+cls.expires_at_length] = \
            token.expires_at.to_bytes(cls.expires_at_length, 'big')
        bytes_wrote += cls.expires_at_length

        bin_token[bytes_wrote:bytes_wrote+cls.impersonation_info_length] = token.impersonation_info
        bytes_wrote += cls.impersonation_info_length

        bin_token[bytes_wrote:bytes_wrote+cls.token_type_length] = token.token_type
        bytes_wrote += cls.token_type_length

        return bin_token

    @classmethod
    def _parse(cls, plaintext):
        obj = cls()
        bytes_read = 0

        obj.organization_id = uuid.UUID(bytes=plaintext[bytes_read:bytes_read+cls.organization_id_length])
        bytes_read += cls.organization_id_length

        obj.user_id = uuid.UUID(bytes=plaintext[bytes_read:bytes_read+cls.user_id_length])
        bytes_read += cls.user_id_length

        obj.client_id = uuid.UUID(bytes=plaintext[bytes_read:bytes_read+cls.client_id_length])
        bytes_read += cls.client_id_length

        obj.mobile_client_id = uuid.UUID(bytes=plaintext[bytes_read:bytes_read+cls.mobile_client_id_length])
        bytes_read += cls.mobile_client_id_length

        obj.user_session_id = uuid.UUID(bytes=plaintext[bytes_read:bytes_read+cls.user_session_id_length])
        bytes_read += cls.user_session_id_length

        obj.client_secret_hash = plaintext[bytes_read:bytes_read+cls.client_secret_hash_length]
        bytes_read += cls.client_secret_hash_length

        obj.mobile_client_secret_hash = plaintext[bytes_read:bytes_read+cls.mobile_client_secret_hash_length]
        bytes_read += cls.mobile_client_secret_hash_length

        obj.issued_at = int.from_bytes(plaintext[bytes_read:bytes_read+cls.issued_at_length], 'big')
        bytes_read += cls.issued_at_length

        obj.expires_at = int.from_bytes(plaintext[bytes_read:bytes_read+cls.expires_at_length], 'big')
        bytes_read += cls.expires_at_length

        obj.impersonation_info = plaintext[bytes_read:bytes_read+cls.impersonation_info_length]
        bytes_read += cls.impersonation_info_length

        obj.token_type = plaintext[bytes_read:bytes_read+cls.token_type_length]
        bytes_read += cls.token_type_length

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
    def generate_client_secret_hash(cls, secret):
        sha = hashlib.sha256()
        sha.update(secret.encode(encoding='utf-8', errors='strict'))
        return sha.digest()

    @classmethod
    def generate_mobile_client_secret_hash(cls, secret):
        sha = hashlib.sha256()
        sha.update(secret.encode(encoding='utf-8', errors='strict'))
        return sha.digest()

    # Organization id getter and setter
    @property
    def organization_id(self):
        pass

    @organization_id.setter
    def organization_id(self, org_id):
        pass

    # User id getter and setter
    @property
    def user_id(self):
        pass

    @user_id.setter
    def user_id(self, user_id):
        pass

    # Client id getter and setter
    @property
    def client_id(self):
        pass

    @client_id.setter
    def client_id(self, client_id):
        pass

    # Mobile Client id getter and setter
    @property
    def mobile_client_id(self):
        pass

    @mobile_client_id.setter
    def mobile_client_id(self, client_id):
        pass

    # User session id getter and setter
    @property
    def user_session_id(self):
        pass

    @user_session_id.setter
    def user_session_id(self, session_id):
        pass

    # Token type getter and setter
    @property
    def token_type(self):
        pass

    @token_type.setter
    def token_type(self, type_of_token):
        pass

    # Client secret hash getter and setter
    @property
    def client_secret_hash(self):
        pass

    @client_secret_hash.setter
    def client_secret_hash(self, secret_hash):
        pass

    # Client secret hash getter and setter
    @property
    def mobile_client_secret_hash(self):
        pass

    @mobile_client_secret_hash.setter
    def mobile_client_secret_hash(self, secret_hash):
        pass

    # is impersonated getter and setter
    @property
    def impersonation_info(self):
        pass

    @impersonation_info.setter
    def impersonation_info(self, info):
        pass

    # issued at getter and setter
    @property
    def issued_at(self):
        pass

    @issued_at.setter
    def issued_at(self, iat):
        pass

    # Expires at getter and setter
    @property
    def expires_at(self):
        pass

    @expires_at.setter
    def expires_at(self, eat):
        pass

    def is_valid(self):
        pass

    def to_dict(self):
        return {
            'organization_id': self.organization_id,
            'user_id': self.user_id,
            'client_id': self.client_id,
            'mobile_client_id': self.mobile_client_id,

            'user_session_id': self.user_session_id,

            'token_type': self.token_type,
            'client_secret_hash': self.client_secret_hash,
            'mobile_client_secret_hash': self.mobile_client_secret_hash,

            'impersonation_info': self.impersonation_info,
            'issued_at': self.issued_at,
            'expired_at': self.expires_at,

            'is_valid': self.is_valid()

        }
