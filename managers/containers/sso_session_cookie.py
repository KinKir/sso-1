from managers.base import BaseManager
from containers.sso_session_cookie.common import SSOSessionCookieInterface


class SSOSessionCookie(BaseManager):
    def validate_cookie(self, cookie: SSOSessionCookieInterface, current_stage: int) -> bool:
        validators = {
            SSOSessionCookieInterface.SSO_SESSION_STAGE_LOGIN_STARTED: self._validate_for_login_started_stage,
            SSOSessionCookieInterface.SSO_SESSION_STAGE_PROVIDER_CHOSE: self._validate_for_provider_chose_stage,
            SSOSessionCookieInterface.SSO_SESSION_STAGE_PROVIDER_EXECUTION: self._validate_for_provider_execution_stage,
            SSOSessionCookieInterface.SSO_SESSION_STAGE_LOGGED_IN: self._validate_for_logged_in_stage
        }
        return validators[current_stage](cookie)

    def _validate_for_login_started_stage(self, cookie: SSOSessionCookieInterface) -> bool:
        pass

    def _validate_for_provider_chose_stage(self, cookie: SSOSessionCookieInterface) -> bool:
        pass

    def _validate_for_provider_execution_stage(self, cookie: SSOSessionCookieInterface) -> bool:
        pass

    def _validate_for_logged_in_stage(self, cookie: SSOSessionCookieInterface) -> bool:
        pass

    def revoke_cookie(self, cookie: SSOSessionCookieInterface) -> object:
        pass

