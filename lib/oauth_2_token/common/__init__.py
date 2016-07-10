from abc import (
    ABCMeta, abstractmethod
)


class TokenInterface(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def deserialize(cls, s, key_retrieval_func):
        pass

    @classmethod
    @abstractmethod
    def serialize(cls, token, keyid, key_retrieval_func):
        pass

    @classmethod
    @abstractmethod
    def generate_client_secret_hash(cls, secret):
        pass

    @classmethod
    @abstractmethod
    def generate_mobile_client_secret_hash(cls, secret):
        pass

    # oauth_2_token id getter and setter
    @property
    @abstractmethod
    def token_id(self):
        pass

    @token_id.setter
    @abstractmethod
    def token_id(self, tid):
        pass

    # refresh oauth_2_token id getter and setter (Only there if this oauth_2_token is refresh oauth_2_token)
    @property
    @abstractmethod
    def refresh_token_id(self):
        pass

    @refresh_token_id.setter
    @abstractmethod
    def refresh_token_id(self, tid):
        pass

    @property
    @abstractmethod
    def tenant_id(self):
        pass

    @tenant_id.setter
    @abstractmethod
    def tenant_id(self, tid):
        pass

    # User id getter and setter
    @property
    @abstractmethod
    def user_id(self):
        pass

    @user_id.setter
    @abstractmethod
    def user_id(self, user_id):
        pass

    # Client id getter and setter
    @property
    @abstractmethod
    def client_id(self):
        pass

    @client_id.setter
    @abstractmethod
    def client_id(self, client_id):
        pass

    # User session id getter and setter
    @property
    @abstractmethod
    def user_session_id(self):
        pass

    @user_session_id.setter
    @abstractmethod
    def user_session_id(self, session_id):
        pass

    # Token type getter and setter
    @property
    @abstractmethod
    def token_type(self):
        pass

    @token_type.setter
    @abstractmethod
    def token_type(self, type_of_token):
        pass

    # Client secret hash getter and setter
    @property
    @abstractmethod
    def client_secret_hash(self):
        pass

    @client_secret_hash.setter
    @abstractmethod
    def client_secret_hash(self, secret_hash):
        pass

    # is impersonated getter and setter
    @property
    @abstractmethod
    def impersonation_info(self):
        pass

    @impersonation_info.setter
    @abstractmethod
    def impersonation_info(self, info):
        pass

    # issued at getter and setter
    @property
    @abstractmethod
    def issued_at(self):
        pass

    @issued_at.setter
    @abstractmethod
    def issued_at(self, iat):
        pass

    # Expires at getter and setter
    @property
    @abstractmethod
    def expires_at(self):
        pass

    @expires_at.setter
    @abstractmethod
    def expires_at(self, eat):
        pass

    @property
    @abstractmethod
    def is_refresh_token(self):
        pass

    @is_refresh_token.setter
    @abstractmethod
    def is_refresh_token(self, v):
        pass

    @property
    @abstractmethod
    def is_impersonated(self):
        pass

    @is_impersonated.setter
    @abstractmethod
    def is_impersonated(self, v):
        pass

    @property
    @abstractmethod
    def is_web(self):
        pass

    @is_web.setter
    @abstractmethod
    def is_web(self, v):
        pass

    @abstractmethod
    def is_valid(self):
        pass

    @abstractmethod
    def to_dict(self):
        pass
