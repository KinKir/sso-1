from db.models.oauth2.code import OAuth2Code
from utils import random_string_generator
from lib.managers.base import Manager
from sqlalchemy import and_

import hashlib

import time
import math

OAUTH_2_CODE_SIZE = 1024


class CodeManager(Manager):

    DEFAULT_EXPIRATION_TIME_DELTA = 5*60

    @staticmethod
    def _hash_code(auth_code):
        hash_obj = hashlib.sha512()
        hash_obj.update(auth_code.encode(encoding='utf-8', errors='strict'))
        return hash_obj.digest().hex()

    def create_code(self, client_id, user_id, redirect_uri):
        auth_code = random_string_generator(OAUTH_2_CODE_SIZE)

        instance = OAuth2Code()
        instance.client_id = client_id
        instance.user_id = user_id
        instance.redirect_uri = redirect_uri
        instance.code_hash = self._hash_code(auth_code)

        instance.created_at = math.floor(time.time())
        instance.expires_at = instance.created_at + self.DEFAULT_EXPIRATION_TIME_DELTA + 1

        self.session.add(instance)
        return instance, auth_code

    def use_code(self, auth_code, redirect_uri, client_id, destroy=True):
        current_time = math.floor(time.time())
        expiration_time = current_time + self.DEFAULT_EXPIRATION_TIME_DELTA
        code_hash = self._hash_code(auth_code)
        instance = self.session.query(OAuth2Code).\
            filter(and_(OAuth2Code.code_hash == code_hash, OAuth2Code.expires_at > expiration_time,
                        OAuth2Code.redirect_uri == redirect_uri,
                        OAuth2Code.client_id == client_id))\
            .one_or_none()

        if instance is None:
            return None
        user_id = instance.user_id

        if destroy:
            self.destroy_code(instance.id)

        return user_id

    def destroy_code(self, auth_code_id):
        instance = self.session.query(OAuth2Code).\
            filter(OAuth2Code.id == auth_code_id).one_or_none()
        if instance is not None:
            self.session.delete(instance)
        return instance


