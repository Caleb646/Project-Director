from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model
from django.apps import apps as django_apps
from django.conf import settings

from gdstorage.storage import GoogleDriveStorage

from .constants import *
from .managers import JobManager, RFIManager, User_RFI_Manager, User_Job_Manager

# Define Google Drive Storage
gd_storage = GoogleDriveStorage()
CustomUser = get_user_model()


class Job(models.Model):
    """
    Each will be accessible to multiple users.
    Syntax to add another user --> user_key.add(User). Docs link: https://docs.djangoproject.com/en/3.1/topics/db/examples/many_to_many/
    """
    name = models.CharField(max_length=50, default=None, unique=True)
    #need to track rfis under a company
    company = models.ForeignKey("authentication.Company", on_delete=models.CASCADE)
    #USER MODEL ALSO has access to this field via CustomUser.get(pk=1).job_set.all()
    assigned_users = models.ManyToManyField(CustomUser, default=[], through="User_Job")
    date_created = models.DateTimeField(auto_now_add=True)

    objects = JobManager()

    class Meta:
        ordering = ["date_created"]

    def __str__(self):
        return self.name

class User_Job(models.Model):
    """
    Serves as an associative table for the User and RFI models. Can be queried by a user instance User.get(pk=1).user_rfi_set.all().
    Docs Link: https://docs.djangoproject.com/en/3.2/topics/db/queries/#m2m-reverse-relationships

    Have to specify the through argument when creating the manytomany field: models.ManyToManyField(CustomUser, through="User_RFI")

    This table will track the notifications for each user in terms of each rfi. So if user A has not opened rfi B they will have a notification but
    user C who has already opened rfi B will not have a notification.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    
    objects = User_Job_Manager()


class RFI(models.Model):
    """
    Note: Only relate RFIs to users not jobs as well. If they are related to jobs
    even if a user has been created they will have to invited to the job to see the RFI.
    Just group by job name.
    """
    #need to track rfis under a company
    company = models.ForeignKey("authentication.Company", on_delete=models.CASCADE)
    #track who sent it
    #use primary key because if the username is ever changed this rfi will be lost
    f_user = models.ForeignKey(CustomUser, default=None, on_delete=models.DO_NOTHING)
    #an rfi could have several people and people have several rfis

    #USER MODEL ALSO has access to this field via CustomUser.get(pk=1).rfi_set.all()
    t_user = models.ManyToManyField(CustomUser, default=[], related_name="rfi_t_user", through="User_RFI")
    #track the job it associated with
    job_key = models.ForeignKey(Job, default=None, on_delete=models.DO_NOTHING)
    subject = models.CharField(max_length=120, default=None)
    body = models.TextField()
    #auto created fields
    last_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    closed = models.BooleanField(default=False)

    objects = RFIManager()

    class Meta:
        ordering = ["date_created"]

    def __str__(self):
        return self.subject

class User_RFI(models.Model):
    """
    Serves as an associative table for the User and RFI models. Can be queried by a user instance User.get(pk=1).user_rfi_set.all().
    Docs Link: https://docs.djangoproject.com/en/3.2/topics/db/queries/#m2m-reverse-relationships

    Have to specify the through argument when creating the manytomany field: models.ManyToManyField(CustomUser, through="User_RFI")

    This table will track the notifications for each user in terms of each rfi. So if user A has not opened rfi B they will have a notification but
    user C who has already opened rfi B will not have a notification.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rfi = models.ForeignKey(RFI, on_delete=models.CASCADE)
    has_unread_responses = models.BooleanField(default=True)

    objects = User_RFI_Manager()


class Response(models.Model):
    """
    Each RFI will have as many responses as neccessary to be able to close it.
    The response will save any attachments internal to the file system
    """
    #track who sent it
    f_user = models.ForeignKey(CustomUser, default=None, on_delete=models.CASCADE)
    rfi = models.ForeignKey(RFI, default=None, on_delete=models.CASCADE)
    subject = models.CharField(max_length=120, default=None)
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date_created"]

    def __str__(self):
        return self.body


class Attachment(models.Model):

    upload = models.FileField(upload_to="attachments", blank=True, storage=gd_storage)
    filename = models.CharField(max_length=120, default="Nameless")
    rfi = models.ForeignKey(RFI, on_delete=models.CASCADE)

    def __str__(self):
        return self.filename
    

    
