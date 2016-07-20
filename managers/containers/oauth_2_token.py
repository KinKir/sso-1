from managers.base import BaseManager
from containers.oauth_2_token.common import OAuth2TokenInterface


class OAuth2TokenManager(BaseManager):
    def validate_token(self, token: OAuth2TokenInterface) -> bool:
        pass

    def revoke_token(self, token: OAuth2TokenInterface) -> object:
        pass


