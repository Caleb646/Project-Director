from django.core.management.base import BaseCommand
from django.contrib.auth.models import  Group, Permission
from django.core.files import File
from django.contrib.auth import get_user_model
from django.conf import settings
from django.apps import apps as django_apps

from PIL import Image
import io
import random
import string
from datetime import date

from ...models import Job, RFI, Response, Attachment, User_Job, User_RFI
from ...constants import *

CustomUser = get_user_model()
Company = django_apps.get_model(settings.COMPANY_MODEL, require_ready=True)

JOBS = [
        {"name" : "Test Job"},

        {"name" : "Second Test Job"}
    ]

RFIS = [
        #Test Job
        {RFI_FROM : "testpm@me.com", RFI_JOB : "Test Job", RFI_TO : ["secondtestsuper@me.com", 'testsuper2@me.com'], RFI_SUBJECT : "Second Test RFI", RFI_BODY : "testing one two three"},
        {RFI_FROM : "testpm@me.com", RFI_JOB : "Test Job", RFI_TO : ["secondtestsuper@me.com", 'testsuper2@me.com'], RFI_SUBJECT : "Second Test RFI", RFI_BODY : "testing one two three"},
        {RFI_FROM : "testpm@me.com", RFI_JOB : "Test Job", RFI_TO : ["secondtestsuper@me.com",], RFI_SUBJECT : "Second Test RFI", RFI_BODY : "testing one two three"},
        {RFI_FROM : "testpm@me.com", RFI_JOB : "Test Job", RFI_TO : ["secondtestsuper@me.com",], RFI_SUBJECT : "Second Test RFI", RFI_BODY : "testing one two three"},
        {RFI_FROM : "testpm@me.com", RFI_JOB : "Test Job", RFI_TO : ["secondtestsuper@me.com", 'testsuper2@me.com'], RFI_SUBJECT : "Second Test RFI", RFI_BODY : "testing one two three"},
        {RFI_FROM : "testpm@me.com", RFI_JOB : "Test Job", RFI_TO : ["secondtestsuper@me.com", 'testsuper2@me.com'], RFI_SUBJECT : "Second Test RFI", RFI_BODY : "testing one two three"},
        {RFI_FROM : "testpm@me.com", RFI_JOB : "Test Job", RFI_TO : ["secondtestsuper@me.com", 'testsuper2@me.com'], RFI_SUBJECT : "Second Test RFI", RFI_BODY : "testing one two three"},

        #Second Test Job
        {RFI_FROM : "secondtestpm@me.com", RFI_JOB : "Second Test Job", RFI_TO : ["testsuper@me.com",'secondtestsuper2@me.com'], RFI_SUBJECT : "First Test RFI", RFI_BODY : "testing one two three"},
        {RFI_FROM : "secondtestpm@me.com", RFI_JOB : "Second Test Job", RFI_TO : ["testsuper@me.com",'secondtestsuper2@me.com'], RFI_SUBJECT : "First Test RFI", RFI_BODY : "testing one two three"},
        {RFI_FROM : "secondtestpm@me.com", RFI_JOB : "Second Test Job", RFI_TO : ["testsuper@me.com",'secondtestsuper2@me.com'], RFI_SUBJECT : "First Test RFI", RFI_BODY : "testing one two three"},
        {RFI_FROM : "secondtestpm@me.com", RFI_JOB : "Second Test Job", RFI_TO : ["testsuper@me.com",], RFI_SUBJECT : "First Test RFI", RFI_BODY : "testing one two three"},
        {RFI_FROM : "secondtestpm@me.com", RFI_JOB : "Second Test Job", RFI_TO : ["testsuper@me.com",], RFI_SUBJECT : "First Test RFI", RFI_BODY : "testing one two three"},
        {RFI_FROM : "secondtestpm@me.com", RFI_JOB : "Second Test Job", RFI_TO : ["testsuper@me.com",], RFI_SUBJECT : "First Test RFI", RFI_BODY : "testing one two three"},
        {RFI_FROM : "secondtestpm@me.com", RFI_JOB : "Second Test Job", RFI_TO : ["testsuper@me.com",'secondtestsuper2@me.com'], RFI_SUBJECT : "First Test RFI", RFI_BODY : "testing one two three"},
        {RFI_FROM : "secondtestpm@me.com", RFI_JOB : "Second Test Job", RFI_TO : ["testsuper@me.com",'secondtestsuper2@me.com'], RFI_SUBJECT : "First Test RFI", RFI_BODY : "testing one two three"},
        {RFI_FROM : "secondtestpm@me.com", RFI_JOB : "Second Test Job", RFI_TO : ["testsuper@me.com",'secondtestsuper2@me.com'], RFI_SUBJECT : "First Test RFI", RFI_BODY : "testing one two three"},
        {RFI_FROM : "secondtestpm@me.com", RFI_JOB : "Second Test Job", RFI_TO : ["testsuper@me.com",'secondtestsuper2@me.com'], RFI_SUBJECT : "First Test RFI", RFI_BODY : "testing one two three"},
    ]

USERS = {
    CustomUser.objects.create_superuser : [

            [{'email' : 'calebthomas646@yahoo.com', 'password' : ADMIN_PASSWORD}, (None, None)],

        ],

    CustomUser.objects.create_user : [

            [{'email' : 'testpm@me.com', 'password' : TEST_USERS_PASSWORD}, (PROJECT_MANAGER_GROUP, "Test Job")],

            [{'email' : 'testsuper@me.com', 'password' : TEST_USERS_PASSWORD}, (SUPER_INTENDENT_GROUP, "Second Test Job")],

            [{'email' : 'testsuper2@me.com', 'password' : TEST_USERS_PASSWORD}, (SUPER_INTENDENT_GROUP, "Second Test Job")],


            [{'email' : 'secondtestpm@me.com', 'password' : TEST_USERS_PASSWORD}, (PROJECT_MANAGER_GROUP, "Second Test Job")],

            [{'email' : 'secondtestsuper@me.com', 'password' : TEST_USERS_PASSWORD}, (SUPER_INTENDENT_GROUP, "Test Job")], 

            [{'email' : 'secondtestsuper2@me.com', 'password' : TEST_USERS_PASSWORD}, (SUPER_INTENDENT_GROUP, "Test Job")],                  
        ]
}

USER_EMAILS = [
    'calebthomas646@yahoo.com',
    'testpm@me.com',
    'testsuper@me.com',
    'testsuper2@me.com',
    'secondtestpm@me.com',
    'secondtestsuper@me.com',
    'secondtestsuper2@me.com',
]

GROUPS = {

    PROJECT_MANAGER_GROUP: {
        #django app model specific permissions
        "job" : ["view"],
        "rfi" : ["add","delete","change","view"],
    },

    SUPER_INTENDENT_GROUP: {
        #django app model specific permissions
        "job" : ["view"],
        "rfi" : ["add","view"],
    },
}



class Command(BaseCommand):
    """
    Sets up all of the test groups, permissions, jobs, rfis, and users. Run after: python manage.py migrate
    """
    help = "Will create all groups, permissions, job, and user needed for testing"
    response_ids = set()
    rfi_ids = set()
    job_ids = set()
    user_ids = set()
    rfis_per_job = 30
    responses_per_rfi = 5
    company = Company.objects.get_or_create(name="Test Company")[0]

    def handle(self, *args, **options):
        self.create_groups()
        for user_type in USERS:
            for users in USERS[user_type]:
                print(users)
                _USER = None
                if not CustomUser.objects.filter(email=users[0]['email']).exists():
                    _USER = user_type(email=users[0]['email'], password=users[0]['password'], company=self.company)
                else:
                    _USER = CustomUser.objects.get(email=users[0]['email'])
                self.user_ids.add(_USER.id)
                if None not in users[1]:
                    self.create_jobs(_USER, users[1][1], )
                    group = Group.objects.get(name=users[1][0])
                    _USER.groups.add(group)

        self.create_rfis()
        self.create_test_responses()
        self.create_test_attachment()


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


    def create_jobs(self, user, job_name):
        """
        Creates all the test jobs that are in the list JOBS:

        @params:
            user: Django auth model User
            job_name: The name of the job associated with the user
        """
        for j in JOBS:
            if j["name"] == job_name:
                if Job.objects.filter(name=job_name).exists():
                    job = Job.objects.get(name=job_name, company=self.company)
                    User_Job.objects.add_users_to_1_job(job, [user.id])

                    self.job_ids.add(job.id)
                else:
                    job = Job.objects.create(name=job_name, company=self.company)
                    User_Job.objects.add_users_to_1_job(job, [user.id])

                    self.job_ids.add(job.id)
    
    def create_rfis(self):
        """
        Creates all of the test RFIs and assigns them to the user that sent it 
        and the user it was sent to.
        """

        num_rfis = RFI.objects.all().count()

        if num_rfis > 100:
            return

        l = len(self.user_ids)
        self.user_ids = list(self.user_ids)
        for job_id in self.job_ids:
            for i in range(self.rfis_per_job):
                from_user_id = self.user_ids[i//l]

                start_dt = date.today().replace(day=1, month=1).toordinal()
                end_dt = date.today().toordinal()
                random_day = date.fromordinal(random.randint(start_dt, end_dt))


                rfi = RFI.objects.create_rfi(
                    f_user_id=from_user_id, 
                    company=self.company, 
                    job_key_id=job_id, 
                    subject=f"Test Job {job_id}", 
                    body=f"Test Job {job_id}",
                    date_created=random_day
                )
                self.rfi_ids.add(rfi.id)
                to_user_ids = set()
                for j in range(len(self.user_ids) - (len(self.user_ids) // 2)):
                    rand_index = random.randint(0, len(self.user_ids) - 1)
                    to_user_ids.add(self.user_ids[rand_index])
                User_RFI.objects.bulk_create_userids_w_rfi(rfi, list(to_user_ids))

    def create_test_responses(self):
        l = len(self.rfi_ids)

        num_responses = Response.objects.all().count()

        if num_responses > 100:
            return

        for rfi_id in self.rfi_ids:
            for i in range(self.responses_per_rfi):
                from_user_id = self.user_ids[i//l]

                start_dt = date.today().replace(day=1, month=1).toordinal()
                end_dt = date.today().toordinal()
                random_day = date.fromordinal(random.randint(start_dt, end_dt))

                response = Response.objects.create(
                    f_user_id=from_user_id, 
                    rfi_id=rfi_id,
                    subject=f"Response by: {from_user_id}", 
                    body=f"Another test from {from_user_id}",
                    date_created=random_day
                )
                self.response_ids.add(response.id)

    def create_test_attachment(self):

        file = io.BytesIO()
        image = Image.new('RGBA', size=(50, 50), color=(200, 200, 0))
        image.save(file, "png")
        file.name = "test image".join(random.choice(string.ascii_lowercase) for _ in range(15))
        file.seek(0)

        for rfi_id in self.rfi_ids:
            rand_int = random.randint(0, 20)
            if rand_int >= 17:
                Attachment.objects.create(upload=File(file, name=file.name), rfi_id=rfi_id)
