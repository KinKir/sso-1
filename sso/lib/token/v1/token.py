from sso.lib.token.common import TokenInterface


class Token(TokenInterface):

    @staticmethod
    def decode(s):
        pass

    @staticmethod
    def encode(token):
        pass

    @staticmethod
    def generate_client_secret_hash(secret):
        pass

    @staticmethod
    def generate_mobile_client_secret_hash(secret):
        pass

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
    def is_impersonated(self):
        pass

    @is_impersonated.setter
    def is_impersonated(self, impersonated):
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

            'is_impersonated': self.is_impersonated,
            'issued_at': self.issued_at,
            'expired_at': self.expires_at,

            'is_valid': self.is_valid()

        }



