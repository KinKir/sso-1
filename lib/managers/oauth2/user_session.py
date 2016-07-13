from lib.managers.base import Manager
from db.models.oauth2.user_session import OAuth2UserSession
from utils import random_string_generator, get_current_time, generate_random_uuid


class UserSessionManager(Manager):

    # 7 Days
    DEFAULT_EXPIRATION_TIME_DELTA = 7 * 24 * 60 * 60

    def create_user_session(self, client_id, user_id, refresh_token_session_id, auth_session_id):
        instance = OAuth2UserSession()
        instance.id = generate_random_uuid()
        instance.user_id = user_id
        instance.refresh_token_session_id = refresh_token_session_id
        instance.client_id = client_id

        if instance.auth_session_id:
            instance.auth_session_id = auth_session_id
            instance.attached_to_auth_session = True

        instance.logout_token = random_string_generator(128)
        instance.created_at = get_current_time()
        instance.expires_at = instance.created_at + self.DEFAULT_EXPIRATION_TIME_DELTA

        self.session.add(instance)
        return instance

    def get_user_sessions(self, user_id, refresh_token_session_id, auth_session_id):
        pass

    def get_user_session(self, user_session_id):
        return self.session.query(OAuth2UserSession). \
            filter(OAuth2UserSession.id == user_session_id).one_or_none()

    def delete_user_session(self, user_session_id):
        instance = self.get_user_session(user_session_id)
        if instance is not None:
            self.session.delete(instance)
        return instance
