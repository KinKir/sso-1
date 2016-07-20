from managers.base import BaseManager


class SSOSessionCookie(BaseManager):
    def validate_cookie(self, cookie, current_stage):
        pass

    def revoke_cookie(self, cookie):
        pass

