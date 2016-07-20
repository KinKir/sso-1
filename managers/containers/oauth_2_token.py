from managers.base import BaseManager


class OAuth2TokenManager(BaseManager):
    def validate_token(self, token):
        pass

    def revoke_token(self, token):
        pass


