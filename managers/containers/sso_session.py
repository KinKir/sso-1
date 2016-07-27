from managers.base import BaseManager
from containers.sso_session.common import SSOSessionInterface


class SSOSession(BaseManager):
    def validate_session(self, cookie: SSOSessionInterface, current_stage: int) -> bool:
        pass

