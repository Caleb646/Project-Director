from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import Group
from django.db import models
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.apps import apps as django_apps

from .utils import track_queries

class CompanyManager(models.Manager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_company(self, name, *args, **kwargs):
        company = self.model(name=name)
        company.save()
        return company  

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    
    def create_user(self, email, password, company, *args, **kwargs):
        """
        Create and save a User with the given email and password.
        """
        group_name: str = kwargs.pop("group_name", None)
        groups: list[int] = kwargs.pop("groups", None)
        jobs: list[int] = kwargs.pop("job_set", None)
        
        if not email:
            raise ValueError(('The Email must be set.'))
        if not company:
            raise ValueError(('The Company must be set.'))
          
        email = self.normalize_email(email)
        user = self.model(email=email, company=company, **kwargs)
        user.set_password(password)
        user.save()
        if groups != None:
            if not isinstance(groups, list):
                raise ValueError(("groups must of type list."))
            #set wipes any other groups
            user.groups.set(groups)
        
        return user

    def create_superuser(self, email, password, company, *args, **kwargs):
        """
        Create and save a SuperUser with the given email and password.
        """
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError(('Superuser must have is_staff=True.'))
        if kwargs.get('is_superuser') is not True:
            raise ValueError(('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, company, *args, **kwargs)

    def reset_password(self, password):
        self.set_password(password)
        self.save()

    def get_by_natural_key(self, email):
        """
        Docs Link: https://docs.djangoproject.com/en/3.1/topics/serialization/#:~:text=It%20is%20for%20these%20reasons%20that%20Django%20provides,use%20an%20integer%20to%20refer%20to%20the%20author.
        """
        return self.get(email=email)


class InviteTokenManager(models.Manager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_token(self, t_user, token, *args, **kwargs):
        token = self.model(t_user=t_user, token=token)
        token.save()
        return token


class EmailManager():
    """
    Link using gmail as email backend: https://medium.com/@_christopher/how-to-send-emails-with-python-django-through-google-smtp-server-for-free-22ea6ea0fb8e
    """
     
    admin_email = settings.EMAIL_HOST_USER

    @classmethod
    def send_email(cls, subject: str, message, to, template_name: str, context: dict) -> bool:
        if type(to) == str:
            to = [to,]
        try: 
            send_mail(subject, message=message, from_email=cls.admin_email, recipient_list=to, html_message=render_to_string(template_name, context), fail_silently=False)
            return True, None
        except Exception as e:
            print("sending an email failed: ", e)
            return False, e  


