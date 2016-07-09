from db.models.oauth2.oauth_2_code import OAUTH_2_CODE_SIZE, OAuth2Code
from utils import random_string_generator
from lib.managers.base import Manager


class OAuth2CodeManager(Manager):

    def create_auth_code(self, client_id, user_id, redirect_uri):
        code = random_string_generator(OAUTH_2_CODE_SIZE)

        instance = OAuth2Code()
        instance.client_id = client_id
        instance.user_id = user_id
        instance.redirect_uri = redirect_uri
        instance.code = code

        self.session.add(instance)
        return instance

    def use_auth_code(self, auth_code, destroy=True):
        pass

    def destroy_auth_code(self, instance_id):
        pass

