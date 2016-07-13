from lib.managers.base import Manager
from db.models.oauth2.refresh_token_session import OAuth2RefreshTokenSession

from sqlalchemy import and_

from utils import get_current_time, generate_random_uuid

_sentinel = object()


class RefreshTokenSessionManager(Manager):

    # 5 years
    DEFAULT_EXPIRATION_TIME_DELTA = 5*12*30*24*60*60

    def create_refresh_token_session(self, client_id, user_id):
        instance = OAuth2RefreshTokenSession()
        instance.id = generate_random_uuid()
        instance.client_id = client_id
        instance.user_id = user_id
        instance.created_at = get_current_time()
        instance.expires_at = instance.created_at + self.DEFAULT_EXPIRATION_TIME_DELTA

        self.session.add(instance)

        return instance

    def get_refresh_token_sessions(self, client_id=_sentinel, user_id=_sentinel):
        query = self.session.query(OAuth2RefreshTokenSession)

        if client_id is _sentinel and user_id is _sentinel:
            return query.all()

        and_arguments = []

        if client_id is not _sentinel:
            and_arguments.append(OAuth2RefreshTokenSession.client_id == client_id)

        if user_id is not _sentinel:
            and_arguments.append(OAuth2RefreshTokenSession.user_id == user_id)

        return query.filter(and_(*and_arguments)).all()

    def get_refresh_token_session(self, refresh_token_session_id):
        return self.session.query(OAuth2RefreshTokenSession).\
            filter(OAuth2RefreshTokenSession.id == refresh_token_session_id).one_or_none()

    def delete_refresh_token_session(self, refresh_token_session_id):
        instance = self.get_refresh_token_session(refresh_token_session_id)
        if instance is not None:
            self.session.delete(instance)
        return instance

