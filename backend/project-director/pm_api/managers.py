
from django.db import models
from django.conf import settings
from django.db.models import Q
from django.contrib.auth import get_user_model

from .utils import track_queries

CustomUser = get_user_model()


class JobManager(models.Manager):

    def filter_by_user_permissions(self, user, company, params=None):
        """
        return a queryset of jobs that the user has permissions to see.
        """

        if user.is_staff or user.is_superuser:
            #return all jobs if user is an admin
            return self.filter(company=company, **params).prefetch_related("assigned_users")
            #user is not an admin so only return jobs that they are assigned to.
        return self.filter(company=company, assigned_users__in=[user], **params).prefetch_related("assigned_users")

class RFIManager(models.Manager):

    def create_rfi(self, *args, **kwargs):

        return self.create(*args, **kwargs)


    def filter_rfis_by_user_permission(self, user, params={}):
        if user.is_staff or user.is_superuser:
            #rfis have to be associated with a company       
            return self.all().filter(company=user.company, **params).select_related("f_user").prefetch_related("t_user")
            #return self.all().filter(**params)
        else:
            #return only the rfis that a user is a part of.
            return self.all().filter(Q(f_user=user) | Q(t_user__in=[user,]), **params).select_related("f_user").prefetch_related("t_user").distinct()


# class ResponseManager(models.Manager):

#     def filter_responses

class User_RFI_Manager(models.Manager):

    def bulk_create_userids_w_rfi(self, rfi, users: list[int]):
        """
        Takes an rfi object and connects it with several users using a 
        bulk create instead of using .add or .set. 

        @Needs to only be used with newly created RFIs because it does
        not check for possible duplicates.
        """
                                    #user_id allows the pk to be the reference
                                    #instead of having to have a user obj
        batch = [self.model(rfi=rfi, user_id=_id) for _id in users]
        if len(batch) == 0:
            return None
        return self.bulk_create(batch, len(batch))
    
    #@track_queries
    def find_users_on_rfi(self, rfi):
        to_user_rows = self.filter(rfi=rfi).select_related("user")
        return [row.user.email for row in to_user_rows]

class User_Job_Manager(models.Manager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def add_users_to_1_job(self, job, users: list[int], *args, **kwargs):
        """
        1. Checks to make sure that the job is not already added to these users.
        2. If they already apart of a certain job that user pk is removed from
        the users list.
        3. If the job is present in all of the users in the user list return None
        4. Else execute the bulk create.
        Takes a job object and connects it with several users using a 
        bulk create instead of using .add or .set. 
        """
        if users is None:
            print(
                f"""\
                The user list was null.\
                File: {self.add_users_to_1_job.__module__}\
                Func: {self.add_users_to_1_job.__name__}\
                """
                )
            return None

        overlapping_users = self.filter(job=job, user__in=users).select_related("user")
        #print("overlapping_users", overlapping_users)
        users = set(users).difference({row.user.id for row in overlapping_users})
        #print("difference between them: ", users)
                                    #user_id allows the pk to be the reference
                                    #instead of having to have a user obj
        batch = [self.model(job=job, user_id=_id) for _id in users]
        if len(batch) == 0:
            return None
        return self.bulk_create(batch, len(batch))

    def add_user_to_multiple_jobs(self, user, jobs: list[int], user_being_created = False):
        """
        1. Checks to make sure that the user is not already added to these jobs.
        2. If they are already apart of a certain job that job pk is removed from
        the jobs list.
        3. If the user is present in all of the jobs in the jobs list return None
        4. Else execute the bulk create.
        Takes a user object and connects it with several jobs using a 
        bulk create instead of using .add or .set. 
        """
        print(f"\njobs {jobs} jobs.\n")
        if jobs is None:
            print(
                f"""
                The job list was null. 
                File: {self.add_user_to_multiple_jobs.__module__}
                Func: {self.add_user_to_multiple_jobs.__name__}
                """
                )
            return None
        #if the user is being created for the first time
        #dont check if they exist on jobs.
        if user_being_created == False:
            overlapping_jobs = self.filter(job__in=jobs, user=user).select_related("job")
            jobs = set(jobs).difference({row.job.id for row in overlapping_jobs}) 
                                        #user_id allows the pk to be the reference
                                        #instead of having to have a user obj
        batch = [self.model(job_id=_id, user=user) for _id in jobs]
        print(f"\nadding user to {batch} jobs.\n")
        if len(batch) == 0:
            return None
        return self.bulk_create(batch, len(batch))