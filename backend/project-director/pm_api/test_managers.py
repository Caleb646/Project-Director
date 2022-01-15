from typing import Union
from django.contrib.auth.models import Permission, Group
from django.conf import settings
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient

import random
import io
from PIL import Image

from .constants import *
from .models import RFI, Job, Response

GROUPS = {
            PROJECT_MANAGER_GROUP: {
                "job" : ["view"],
                "rfi" : ["add","delete","change","view"],
            },
            SUPER_INTENDENT_GROUP: {
                "job" : ["view"],
                "rfi" : ["add","view"],
            },
        }

CustomUser = get_user_model()
BaseTestManager = settings.IMPORT_STRING(settings.BASE_TEST_MANAGER)


class PmTestManager(BaseTestManager):

    def __init__(self, client: APIClient, test_case: TestCase) -> None:
        BaseTestManager.__init__(self, client, test_case)

    def create_groups(self):
        """
        Creates all of the groups and their specific permissions
        """
        for group_name in GROUPS:

            new_group, created = Group.objects.get_or_create(name=group_name)
            for app_model in GROUPS[group_name]:

                for permission_name in GROUPS[group_name][app_model]:

                    name = "Can {} {}".format(permission_name, app_model)

                    model_add_perm = Permission.objects.get_or_create(name=name)
                    new_group.permissions.add(model_add_perm[0])

    def create_job(self, user=None, users: Union[CustomUser, None]=None):
        data = {
            "name": f"Test {random.randint(1, 1000)}{random.randint(1, 1000)}",
            "company": self.company,
        }
        job = Job.objects.create(**data)
        if isinstance(user, CustomUser):
            job.assigned_users.add(user)
        if isinstance(users, list):
            for u in users:
                job.assigned_users.add(u)
        return job

    def create_rfi(self, _from, job, to):
        data = {
            "f_user": _from,
            "job_key": job,
            "company": self.company,
            "subject": "UnitTest",
            "body": "UnitTest"
        }
        rfi = RFI(**data)
        rfi.save()
        rfi.t_user.add(to)
        return rfi

    def create_response(self, from_user, rfi_key):
        data = {
            "f_user": from_user, 
            "rfi": rfi_key,
            "subject": "UnitTest",
            "body": "testing"
            }
        return Response.objects.create(**data)

    def create_image(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(200, 200), color=(200, 200, 0))
        image.save(file, "png")
        file.name = "test image"
        file.seek(0)
        return file

  