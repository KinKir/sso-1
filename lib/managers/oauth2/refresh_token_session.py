import math
import time

from lib.managers.base import Manager
from db.models.oauth2.refresh_token_session import OAuth2RefreshTokenSession

from sqlalchemy import and_


class RefreshTokenSessionManager(Manager):

    # 5 years
    DEFAULT_EXPIRATION_TIME_DELTA = 5*12*30*24*60*60

    def create_refresh_token_session(self, client_id, user_id):
        instance = OAuth2RefreshTokenSession()
        instance.client_id = client_id
        instance.user_id = user_id
        instance.created_at = math.floor(time.time())
        instance.expires_at = instance.created_at + self.DEFAULT_EXPIRATION_TIME_DELTA

        self.session.add(instance)

    def get_refresh_token_sessions(self, client_id, user_id):
        query = self.session.query(OAuth2RefreshTokenSession)

        if client_id is not None and user_id is not None:
            query.filter(and_(OAuth2RefreshTokenSession.client_id == client_id,
                              OAuth2RefreshTokenSession == user_id))
        elif client_id is not None:
            query.filter(OAuth2RefreshTokenSession.client_id == client_id)
        elif user_id is not None:
            query.filter(OAuth2RefreshTokenSession.user_id == user_id)

        return query.all()

    def get_refresh_token_session(self, refresh_token_session_id):
        return self.session.query(OAuth2RefreshTokenSession).\
            filter(OAuth2RefreshTokenSession.id == refresh_token_session_id).one_or_none()

    def delete_refresh_token_session(self, refresh_token_session_id):
        instance = self.get_refresh_token_session(refresh_token_session_id)
        self.session.delete(instance)

