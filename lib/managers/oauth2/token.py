from lib.managers.base import Manager
from db.models.oauth2.user_session import UserSession
from db.models.oauth2.refresh_token_session import RefreshTokenSession


class TokenManager(Manager):
    def create_token(self, client, user, is_refresh_token=False):
        pass

    def revoke_token(self, token):
        pass

    def is_token_valid(self, token):
        pass
