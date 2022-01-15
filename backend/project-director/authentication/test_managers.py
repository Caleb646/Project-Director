from django.conf import settings
from django.contrib.auth import get_user_model
from django.apps import apps as django_apps
from django.test import TestCase

from rest_framework.test import APIClient

import random
import string
import json

from .settings import ACCESS_TOKEN, REFRESH_TOKEN

CustomUser = get_user_model()
InviteToken = django_apps.get_model(settings.TOKEN_AUTH_MODEL, require_ready=True)
Company = django_apps.get_model(settings.COMPANY_MODEL, require_ready=True)
EmailManager = settings.IMPORT_STRING(settings.EMAIL_MANAGER)


class BaseTestManager:
    def __init__(self, client: APIClient, test_case: TestCase):
        self.client = client
        self.test_case = test_case
        self.company = Company.objects.create_company(name="Test Company")
        self.base_url = '/api/d1'
        self.request_types = {
            "post": self.client.post,
            "get": self.client.get,
            "patch": self.client.patch,
        }
    def user_forbidden(self, response):
        #print("\n\nresponse cookies: ", response.__dict__["cookies"].__dict__, "\n\n")
        self.test_case.assertEqual(response.status_code, 401)
        self.test_case.assertEqual(response.__dict__["cookies"].get(REFRESH_TOKEN), None)
        #self.test_case.assertEqual(response.__dict__["cookies"].get(ACCESS_TOKEN), None)
        self.test_case.assertEqual(json.loads(response.content).get(ACCESS_TOKEN, None), None)
        #self.test_case.assertEqual(response.__dict__["cookies"].get("csrftoken", None), None)

    def user_allowed(self, response):
        """
        Check that an authenticated user has both a session id and an csrftoken.
        """
        #print("\n\nallowed response cookies: ", response.__dict__["cookies"].get(REFRESH_TOKEN), "\n\n")
        #print("\n\nresponse cookies: ", response.content, "\n\n")
        self.test_case.assertEqual(response.status_code, 200)
        self.test_case.assertNotEqual(response.__dict__["cookies"].get(REFRESH_TOKEN), None)
        #self.test_case.assertNotEqual(response.__dict__["cookies"].get(ACCESS_TOKEN), None)
        self.test_case.assertNotEqual(json.loads(response.content).get(ACCESS_TOKEN, None), None)
        #self.test_case.assertNotEqual(response.__dict__["cookies"].get("csrftoken", None), None)
    
    def user_exists(self, value):
        return CustomUser.objects.all().filter(email=value).exists()

    def create_random_user(self, super_user=False, groups=None):
        rand_email = ''.join(random.choice(string.ascii_lowercase) for _ in range(10)) + "@test.com"
        rand_password = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
        if super_user:
            return CustomUser.objects.create_superuser(rand_email, rand_password, self.company, groups=groups), rand_password
        return CustomUser.objects.create_user(rand_email, rand_password, self.company, groups=groups), rand_password

    def make_request(self, request_type, relative_url, data: dict = None, access_token=None):
        if access_token != None:
            self.client.credentials(HTTP_AUTHORIZATION="Bearer "+access_token)
        if data == None:
            return self.request_types[request_type](relative_url, HTTP_ACCEPT="application/json")
        return self.request_types[request_type](relative_url, data, HTTP_ACCEPT="application/json")

    def get_access_token(self, valid_email, valid_password):
        response = self.make_request("post", f"{self.base_url}/auth/user/login/", {"email": valid_email, "password": valid_password})
        return json.loads(response.content)[ACCESS_TOKEN]


class AuthTestManager(BaseTestManager):

    def __init__(self, client: APIClient, test_case: TestCase):
        BaseTestManager.__init__(self, client, test_case)

    def create_random_token(self, user):
        return InviteToken.objects.create_token(user, ''.join(random.choice(string.ascii_lowercase) for _ in range(10)))

