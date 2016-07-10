from db.models.oauth2.oauth_2_code import OAUTH_2_CODE_SIZE, OAuth2Code, DEFAULT_EXPIRATION_TIME_DELTA
from utils import random_string_generator
from lib.managers.base import Manager
from sqlalchemy import and_

import time
import math


class CodeManager(Manager):

    def create_code(self, client_id, user_id, redirect_uri):
        code = random_string_generator(OAUTH_2_CODE_SIZE)

        instance = OAuth2Code()
        instance.client_id = client_id
        instance.user_id = user_id
        instance.redirect_uri = redirect_uri
        instance.code = code

        self.session.add(instance)
        return instance

    def use_code(self, auth_code, redirect_uri, client_id, destroy=True):
        current_time = math.floor(time.time())
        expiration_time = current_time + DEFAULT_EXPIRATION_TIME_DELTA
        instance = self.session.query(OAuth2Code).\
            filter(and_(OAuth2Code.code == auth_code, OAuth2Code.expires_at > expiration_time,
                        OAuth2Code.redirect_uri == redirect_uri,
                        OAuth2Code.client_id == client_id))\
            .one_or_none()

        if instance is None:
            return None
        user_id = instance.user_id

        if destroy:
            self.destroy_code(instance)

        return user_id

    def destroy_code(self, instance):
        self.session.delete(instance)

