from lib.managers.base import Manager


class UserSessionManager(Manager):
    def create_user_session(self, user_id, refresh_token_session_id):
        pass

    def get_user_sessions(self, user_id, refresh_token_session_id):
        pass

    def get_user_session(self, user_id, refresh_token_session_id, user_session_id):
        pass

    def delete_user_session(self, user_id, refresh_token_session_id, user_session_id):
        pass
