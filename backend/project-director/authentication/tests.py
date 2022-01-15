from django.test import TestCase
from django.contrib.auth.models import Permission, Group

from rest_framework.test import APIClient

import json

from .test_managers import AuthTestManager
from .settings import REFRESH_TOKEN, ACCESS_TOKEN

class AuthTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.tm = AuthTestManager(self.client, self)
        self.user, self.rand_password = self.tm.create_random_user()
        self.token = self.tm.create_random_token(self.user)
        self.access_token = self.tm.get_access_token(self.user.email, self.rand_password)
      
    def test_user_login_logout(self):
        #bad login request
        response = self.tm.make_request("post", "/api/auth/user/login/", {"password": self.rand_password})
        self.assertEqual(response.status_code, 400)
        #bad login request
        response = self.tm.make_request("post", "/api/auth/user/login/", {"email": "123123asdf", "password": self.rand_password})
        self.tm.user_forbidden(response)
        #good login request
        response = self.tm.make_request("post", "/api/auth/user/login/", {"email": self.user.email, "password": self.rand_password})
        self.tm.user_allowed(response)
        #test refresh
        response = self.client.post("/api/auth/token/refresh/", format="json")
        #self.tm.user_allowed(response)
        #test logout
        response = self.tm.make_request("post", "/api/auth/user/logout/", access_token=self.access_token)
        self.assertEqual(response.status_code, 200)

    def test_user_register(self):
        #bad register request
        response = self.tm.make_request("post", "/api/auth/user/register/", {"password": self.rand_password})
        self.assertEqual(response.status_code, 400)
        #good register request
        response = self.tm.make_request("post", "/api/auth/user/register/", {"email": "testing@to.com"})
        self.assertEqual(response.status_code, 200)
        #bad confirm register request
        response = self.tm.make_request("post", "/api/auth/user/confirm_registration/", {"email": ""})
        self.assertEqual(response.status_code, 400)
        #good confirm register request
        response = self.tm.make_request("post", "/api/auth/user/confirm_registration/", {"email": "testing@to.com", "password": self.rand_password})
        self.assertEqual(response.status_code, 200)
        #check that user was created
        self.assertEqual(self.tm.user_exists("testing@to.com"), True)
    
    def test_token_login(self):
        #bad token login
        response = self.tm.make_request("post", "/api/auth/invite-token/login/", {"password": self.rand_password, "token": self.token.token})
        self.assertEqual(response.status_code, 400)
        #forbidden token login
        response = self.tm.make_request("post", "/api/auth/invite-token/login/", {"email": "asdfasdfasdawe", "password": self.rand_password, "token": self.token.token})
        self.tm.user_forbidden(response)
        #good token login
        response = self.tm.make_request("post", "/api/auth/invite-token/login/", {"email": self.user.email, "password": self.rand_password, "token": self.token.token})
        #print("\n Response: ", response.content, "\n")
        #print("\n User email: ", self.user.email, "\n")
        #print("\n Token: ", self.token.token, "\n")
        self.tm.user_allowed(response)

    def test_who_am_i(self):
        response = self.tm.make_request("get", "/api/auth/me/", access_token=self.access_token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)["results"], {"email": self.user.email})


