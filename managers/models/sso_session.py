from db.models.sso_session import SSOSession
from managers.base import BaseManager
from utils import get_current_time, generate_random_uuid

_sentinel = object()


class SSOSessionManager(BaseManager):

    # 10 days
    DEFAULT_EXPIRATION_TIME_DELTA = 10*24*60*60

    def create_sso_session(self, user_id):
        instance = SSOSession()
        instance.id = generate_random_uuid()
        instance.user_id = user_id
        instance.created_at = get_current_time()
        instance.expires_at = instance.created_at + self.DEFAULT_EXPIRATION_TIME_DELTA

        self.session.add(instance)

        return instance

    def get_sso_sessions(self, user_id=_sentinel):
        query = self.session.query(SSOSession)

        if user_id is _sentinel:
            return query.all()
        else:
            return query.filter(SSOSession.user_id == user_id)

    def get_sso_session(self, sso_session_id):
        return self.session.query(SSOSession).\
            filter(SSOSession.id == sso_session_id).one_or_none()

    def delete_sso_session(self, sso_session_id):
        instance = self.get_sso_session(sso_session_id)
        if instance is not None:
            self.session.delete(instance)
        return instance

