from lib.managers.base import Manager


class RefreshTokenSessionManager(Manager):
    def create_refresh_token_session(self, user_id):
        pass

    def get_refresh_token_sessions(self, user_id):
        pass

    def get_refresh_token_session(self, user_id, refresh_token_session_id):
        pass

    def delete_refresh_token_session(self, user_id, refresh_token_session_id):
        pass

