from lib.managers.base import Manager
from lib.managers.oauth2.refresh_token_session import RefreshTokenSessionManager
from lib.managers.oauth2.user_session import UserSessionManager

from lib.oauth_2_token.v1.token import Token as Token_v1

from utils import generate_random_uuid


class TokenManager(Manager):

    VERSION_SEPARATOR = '_'

    version_map = {
        'v1': Token_v1
    }

    allowed_token_versions_for_encryption = ['v1']

    allowed_token_versions_for_decryption = ['v1']

    latest_version = 'v1'

    def __init__(self, session):
        super(TokenManager, self).__init__(session)
        self._refresh_token_session_manager = RefreshTokenSessionManager(session)
        self._user_session_manager = UserSessionManager(session)

    def create_user_token(self, client, user, refresh_token_session_id, auth_session_id, tenant_id, user_session_id, create_session=True):
        instance = self.version_map[self.latest_version]()

        if instance.auth_session_id is not None:
            instance.auth_session_id = auth_session_id

        instance.token_id = generate_random_uuid()
        instance.user_id = user.id
        instance.client_id = client.id
        instance.client_secret_hash = client.secret_hash
        instance.refresh_token_session_id = refresh_token_session_id
        instance.tenant_id = tenant_id
        if create_session:
            user_session = self._user_session_manager.\
                create_user_session(client.id, user.id, refresh_token_session_id, auth_session_id)
            instance.user_session_id = user_session.id
        else:
            instance.user_session_id = user_session_id

        instance.is_impersonated = False
        instance.is_refresh_token = False

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

