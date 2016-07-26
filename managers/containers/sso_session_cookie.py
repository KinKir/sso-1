from managers.base import BaseManager
from containers.sso_session_cookie.common import SSOSessionCookieInterface


class SSOSessionCookie(BaseManager):
    def validate_cookie(self, cookie: SSOSessionCookieInterface, current_stage: int) -> bool:
        pass

