from lib.managers.base import BaseManager
from lib.managers.oauth2.refresh_token_session import RefreshTokenSessionManager
from lib.managers.oauth2.user_session import UserSessionManager
from lib.managers.keyring import KeyRingManager

from lib.oauth_2_token.v1.token import Token as Token_v1

from utils import generate_random_uuid, get_current_time


class TokenManager(BaseManager):

    VERSION_SEPARATOR = '_'

    # 3 days
    DEFAULT_TOKEN_EXPIRATION_TIME_DELTA = 3*24*60*60

    TOKEN_VERSION_MAP = {
        'v1': Token_v1
    }

    ALLOWED_TOKEN_VERSIONS_FOR_ENCRYPTION = ['v1']

    ALLOWED_TOKEN_VERSIONS_FOR_DECRYPTION = ['v1']

    LATEST_TOKEN_VERSION = 'v1'

    def __init__(self, session, master_key):
        super(TokenManager, self).__init__(session)
        self._refresh_token_session_manager = RefreshTokenSessionManager(session)
        self._user_session_manager = UserSessionManager(session)
        self._keyring_manager = KeyRingManager(session, master_key)

    def create_user_token(self, client, user, refresh_token_session_id, auth_session_id, tenant_id, user_session_id,
                          create_session=True):
        token_cls = self.TOKEN_VERSION_MAP[self.LATEST_TOKEN_VERSION]
        instance = token_cls()

        if instance.auth_session_id is not None:
            instance.auth_session_id = auth_session_id

        instance.token_id = generate_random_uuid()
        instance.user_id = user.id
        instance.client_id = client.id
        instance.client_secret_hash = bytes.fromhex(client.secret_hash)
        instance.refresh_token_session_id = refresh_token_session_id
        instance.tenant_id = tenant_id
        if create_session:
            user_session = self._user_session_manager. \
                create_user_session(client.id, user.id, refresh_token_session_id, auth_session_id)
            instance.user_session_id = user_session.id
        else:
            instance.user_session_id = user_session_id

        instance.is_impersonated = False
        instance.is_refresh_token = False
        instance.is_web = True

        instance.issued_at = get_current_time()
        instance.expires_at = get_current_time() + self.DEFAULT_TOKEN_EXPIRATION_TIME_DELTA
        return self.LATEST_TOKEN_VERSION, instance

    def create_refresh_token(self, client, user, tenant_id, refresh_token_session_id, create_session=True):
        token_cls = self.TOKEN_VERSION_MAP[self.LATEST_TOKEN_VERSION]
        instance = token_cls()

        instance.token_id = generate_random_uuid()
        instance.user_id = user.id
        instance.client_id = client.id
        instance.client_secret_hash = bytes.fromhex(client.secret_hash)
        instance.tenant_id = tenant_id
        if create_session:
            refresh_token_session = self._refresh_token_session_manager. \
                create_refresh_token_session(client.id, user.id)
            instance.refresh_token_session_id = refresh_token_session.id
        else:
            instance.refresh_token_session_id = refresh_token_session_id

        instance.is_impersonated = False
        instance.is_refresh_token = True
        instance.is_web = True

        instance.issued_at = get_current_time()
        instance.expires_at = get_current_time() + self.DEFAULT_TOKEN_EXPIRATION_TIME_DELTA
        return self.LATEST_TOKEN_VERSION, instance

    def revoke_token_session(self, token):
        if token.is_refresh_token:
            self._refresh_token_session_manager.delete_refresh_token_session(token.refresh_token_session_id)
        else:
            self._user_session_manager.delete_user_session(token.user_session_id)

    def create_user_token_and_serialize(self, client, user, refresh_token_session_id, auth_session_id, tenant_id,
                                        user_session_id, create_session=True):
        token_version, instance = self.create_user_token(client, user, refresh_token_session_id, auth_session_id,
                                                         tenant_id, user_session_id, create_session)
        return self.serialize_token(token_version, instance)

    def create_refresh_token_and_serialize(self, client, user, tenant_id, refresh_token_session_id,
                                           create_session=True):
        token_version, instance = self.create_refresh_token(client, user, tenant_id, refresh_token_session_id,
                                                            create_session)
        return self.serialize_token(token_version, instance)

    def serialize_token(self, token_version, instance):
        key, key_container = self._keyring_manager.generate_and_save_key(instance.expires_at_length)
        token_cls = self.TOKEN_VERSION_MAP.get(token_version)
        if token_cls is None:
            # TODO: raise an error
            pass
        serialized_token = token_cls.serialize(instance, key_container.id, lambda x: key)
        return self._attach_token_version(self.LATEST_TOKEN_VERSION, serialized_token)

    def deserialize_token(self, serialized_token_with_version):
        version, serialized_token = self._detach_token_version(serialized_token_with_version)
        token_cls = self.TOKEN_VERSION_MAP.get(version)
        if token_cls is None:
            # TODO: raise an error
            pass
        keyid, token = token_cls.deserialize(serialized_token, self._keyring_manager.get_key)
        return version, keyid, token

    def is_token_valid(self, token):
        pass

    def _detach_token_version(self, serialized_token_with_version):
        splinters = serialized_token_with_version.split(sep=self.VERSION_SEPARATOR)
        return splinters[0], splinters[1]

    def _attach_token_version(self, version, serialized_token):
        return version + self.VERSION_SEPARATOR + serialized_token
