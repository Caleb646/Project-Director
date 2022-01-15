from django.test import TestCase
from django.contrib.auth.models import Permission, Group
from django.contrib.auth import get_user_model
from django.apps import apps as django_apps
from django.conf import settings

from rest_framework.test import APIClient

import json

from .test_managers import PmTestManager
from .models import RFI
from .constants import *


CustomUser = get_user_model()
InviteToken = django_apps.get_model(settings.TOKEN_AUTH_MODEL, require_ready=True)
EmailManager = settings.IMPORT_STRING(settings.EMAIL_MANAGER)

base_url_prefix = "/api/d1"

class RfiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.tm = PmTestManager(self.client, self)
        self.tm.create_groups()
        self.from_user, self.from_password = self.tm.create_random_user()
        self.to_user, self.to_password = self.tm.create_random_user()
        self.job = self.tm.create_job(self.from_user)
        self.rfi = self.tm.create_rfi(self.from_user, self.job, self.to_user)
        self.access_token = self.tm.get_access_token(self.from_user.email, self.from_password)
        self.set_access_token = self.tm.client.credentials(HTTP_AUTHORIZATION="Bearer "+self.access_token)

    def test_rfi_detail(self):

        response = self.client.get(f"{base_url_prefix}/pm/rfi/{self.rfi.id}/")
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(content['results']["id"], self.rfi.id)

    def test_rfi_list(self):
        response = self.client.get(f"{base_url_prefix}/pm/rfi/")
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(content["results"][0]["id"], self.rfi.id)

    def test_rfi_create(self):
        #create rfi
        image = self.tm.create_image()
        data = {
            "job_key": self.job.id,
            #"t_user":  json.dumps([{"id":self.to_user.id,"groups":[{"name":"Superintendent"}],"email":self.to_user.email}]),
            "t_user":  self.to_user.id,
            "subject": "testing image upload",
            "body": "testing",
            "attachments": image
        }
        response = self.client.post(f"{base_url_prefix}/pm/rfi/", data, format="multipart")
        #print("rfi response: ", response)
        content = json.loads(response.content)
        #print("rfi content: ", content)
        rfi = RFI.objects.get(pk=content["results"]["id"])
        self.assertEqual(response.status_code, 201)

        #test image was uploaded
        response = self.client.get(f"{base_url_prefix}/pm/attachment/{rfi.id}/preview/")
        content = json.loads(response.content)
        self.assertEqual(content["results"][0]["id"], 1)

        #tests if the user was added to the job
        self.assertEqual(self.job.assigned_users.filter(pk=self.to_user.id).exists(), True)

    def test_rfi_update(self):

        #make another call with the auth token
        response = self.client.put(f"{base_url_prefix}/pm/rfi/{self.rfi.id}/", {"closed": True})
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        #check to see if the updated field was updated.
        self.assertEqual(content["results"]["closed"], True, f"content: {content}")

class UserViewsTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.tm = PmTestManager(self.client, self)
        self.tm.create_groups()
        self.from_user, self.from_password = self.tm.create_random_user()
        self.to_user, self.to_password = self.tm.create_random_user()
        self.job = self.tm.create_job(self.from_user)
        self.rfi = self.tm.create_rfi(self.from_user, self.job, self.to_user)
        self.access_token = self.tm.get_access_token(self.from_user.email, self.from_password)
        self.set_access_token = self.tm.client.credentials(HTTP_AUTHORIZATION="Bearer "+self.access_token)

    def test_user_list(self):
        response = self.client.get(f"{base_url_prefix}/pm/user/")
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        #there should only be one user
        self.assertEqual(content['results'][0]['id'], self.from_user.id)

    def test_user_create(self):

        #print(f"\njob id: {self.job.id}")

        _data = {
           "first_name": "test",
           "last_name": "tester",
           "groups": 1,
           "email": "testing@test.com",
           "job_set": [self.job.id]
       }
        response = self.client.post(f"{base_url_prefix}/pm/user/invite_user/", _data)
        email = json.loads(response.content)['results']['email']
        self.assertEqual(response.status_code, 201)
        content = json.loads(response.content)
        #there should only be one user
        self.assertEqual(content['results']['email'], "testing@test.com")

        #check that the login token was created
        token = InviteToken.objects.all().first()
        self.assertIsNotNone(token)

        #check that the correct user was added to the invite token
        to_user = CustomUser.objects.get(email=email)
        self.assertEqual(to_user.id, token.t_user.id)

        #check that the user was added to the correct job
        self.assertEqual(self.job.assigned_users.filter(pk=to_user.id).exists(), True)

    def test_token_login(self):

        _data = {
           "first_name": "test",
           "last_name": "tester",
           "group_name": PROJECT_MANAGER_GROUP,
           "email": "testing@test.com",
           "job_key": [self.job.id]
       }
        #create user and grab the token
        response = self.client.post(f"{base_url_prefix}/pm/user/invite_user/", _data)
        #print("response:   ", response)
        content = json.loads(response.content)
        #print(f"user content: {content}")
        to_user = CustomUser.objects.get(email=content['results']['email'])
        token = InviteToken.objects.all().first()
        #check with no token
        data = {
            "email": to_user.email,
            "password": "1234"
        }
        response = self.client.post(f"{base_url_prefix}/auth/invite-token/login/", data)
        self.assertEqual(response.status_code, 400)
        #check with wrong token
        data = {
            "email": to_user.email,
            "token": "lkasjdglkasjdflk;",
            "password": "1234"
        }
        response = self.client.post(f"{base_url_prefix}/auth/invite-token/login/", data)
        self.assertEqual(response.status_code, 401)
        #use valid token
        data = {
            "email": to_user.email,
            "token": token.token,
            "password": "1234"
        }
        response = self.client.post(f"{base_url_prefix}/auth/invite-token/login/", data)
        self.assertEqual(response.status_code, 200)
        self.tm.user_allowed(response)

    def test_group_list(self):
        response = self.client.get(f"{base_url_prefix}/pm/group/")
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        
        #check that all test groups were created
        #print(f"  groups content   : {content}")
        self.assertEqual(content["results"][0]["name"], 'Project_Manager')
        self.assertEqual(content["results"][1]["name"], 'Superintendent')

class ResponseViewsTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.tm = PmTestManager(self.client, self)
        self.tm.create_groups()
        self.from_user, self.from_password = self.tm.create_random_user()
        self.to_user, self.to_password = self.tm.create_random_user()
        self.job = self.tm.create_job(self.from_user)
        self.rfi = self.tm.create_rfi(self.from_user, self.job, self.to_user)
        self.first_response = self.tm.create_response(self.from_user, self.rfi)
        self.access_token = self.tm.get_access_token(self.from_user.email, self.from_password)
        self.set_access_token = self.tm.client.credentials(HTTP_AUTHORIZATION="Bearer "+self.access_token)

    def test_response_list(self):
        response = self.client.get(f"{base_url_prefix}/pm/response/?rfi={self.rfi.id}")
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        #there should only be one user
        self.assertEqual(content['results'][0]['id'], self.first_response.id)

    def test_response_create(self):
        data = {
            "rfi": self.rfi.id,
            "subject": "Test subject",
            "body": "another test",
        }
        response = self.client.post(f"{base_url_prefix}/pm/response/", data)
        self.assertEqual(response.status_code, 201)
        content = json.loads(response.content)
        #body should match the above
        self.assertEqual(content['results']['body'], "another test")

class JobViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.tm = PmTestManager(self.client, self)
        self.tm.create_groups()
        self.from_user, self.from_password = self.tm.create_random_user(super_user=True)
        self.to_user, self.to_password = self.tm.create_random_user(groups=[1])
        #add both users to the job
        self.job = self.tm.create_job(users=[self.from_user, self.to_user])
        #create a second job without adding the project manager
        self.second_job = self.tm.create_job()
        self.rfi = self.tm.create_rfi(self.from_user, self.job, self.to_user)
        self.first_response = self.tm.create_response(self.from_user, self.rfi)
        self.admin_token = self.tm.get_access_token(self.from_user.email, self.from_password)
        self.project_manager_token = self.tm.get_access_token(self.to_user.email, self.to_password)
    
    def test_jobs_list(self):

        #project manager should only have access to the jobs they have been added to
        self.tm.client.credentials(HTTP_AUTHORIZATION="Bearer "+self.project_manager_token)
        response = self.client.get(f"{base_url_prefix}/pm/job/")
        self.assertEqual(response.status_code, 200)
        #print("job response: ", response)
        content = json.loads(response.content)
        #print("job content: ", content)
        self.assertEqual(content["results"][0]["id"], self.job.id)
        self.assertEqual(len(content["results"]), 1)

        #super user should get access to all jobs
        self.tm.client.credentials(HTTP_AUTHORIZATION="Bearer "+self.admin_token)
        response = self.client.get(f"{base_url_prefix}/pm/job/")
        self.assertEqual(response.status_code, 200)
        #print("job response: ", response)
        content = json.loads(response.content)
        #print("job content: ", content)
        self.assertEqual(len(content["results"]), 2)

