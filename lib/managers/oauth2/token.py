from lib.managers.base import Manager
from lib.managers.oauth2.refresh_token_session import RefreshTokenSessionManager
from lib.managers.oauth2.user_session import UserSessionManager


class TokenManager(Manager):
    def create_user_token(self, client, user, refresh_token_session_id, auth_session_id, create_session=True):
        pass

    def create_refresh_token(self, client, user, create_session=True):
        pass

    def get_refresh_token(self, client, user):
        pass

    def revoke_token(self, token):
        pass

    def is_token_valid(self, token):
        pass
