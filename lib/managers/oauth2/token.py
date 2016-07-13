from lib.managers.base import Manager
from lib.managers.oauth2.refresh_token_session import RefreshTokenSessionManager
from lib.managers.oauth2.user_session import UserSessionManager


class TokenManager(Manager):

    VERSION_SEPARATOR = '_'

    allowed_encryption_versions = {
        'v1': ''
    }

    def __init__(self, session):
        super(TokenManager, self).__init__(session)
        self._refresh_token_session_manager = RefreshTokenSessionManager(session)
        self._user_session_manager = UserSessionManager(session)

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

    def _detach_token_version(self, token):
        splinters = token.split(sep=self.VERSION_SEPARATOR)
        return splinters[0], splinters[1]

    def _attach_token_version(self, version, token):
        return version + self.VERSION_SEPARATOR + token

