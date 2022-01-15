from collections import OrderedDict
from typing import Union
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.apps import apps as django_apps
from django.conf import settings
from django.utils import timezone

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from datetime import datetime

from .models import RFI, Job, Response as MyResponse, Attachment, User_RFI, User_Job
from .utils import rand_password
from .constants import *



CustomUser = get_user_model()
InviteToken = django_apps.get_model(settings.TOKEN_AUTH_MODEL, require_ready=True)
Company = django_apps.get_model(settings.COMPANY_MODEL, require_ready=True)
EmailManager = settings.IMPORT_STRING(settings.EMAIL_MANAGER)

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("id", "name")

class AttachmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attachment
        fields = "__all__"


class JobSerializer(serializers.ModelSerializer):
    """
    This a dynamic serializer. It allows for the fields to be set on initialization.
    """
    #user_key = UserSerializer(many=True)
    def __init__(self, instance=None, data=None, **kwargs):
        fields = kwargs.pop("fields", None)
        partial = kwargs.pop("partial", False)
        super().__init__(instance=instance, data=data, partial=partial, **kwargs)
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            # Drop any fields that are not specified in the `fields` argument.
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = Job
        #fields = ("id", JOB_NAME, DATE_START, USERS)
        fields = ("id", "name", "date_created")
        extra_kwargs = {
            #have to be set read_only to false to show up in validated_data
            'id': {'validators': [], "required": False, "read_only": False},
            'name': {'validators': [], "required": False},   
        }

class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ("id", "name")
        extra_kwargs = {
            #have to be set read_only to false to show up in validated_data
            'id': {'validators': [], "required": False, "read_only": False},
            'name': {'validators': [], "required": False},   
        }


class UserSerializer(serializers.ModelSerializer):
    """
    This a dynamic serializer. It allows for the fields to be set on initialization.
    """
                                        #makes these two not required and can be null
    groups = GroupSerializer(many=True, read_only=True, **{'validators': [], "required": False, 'allow_null': True})
    job_set = JobSerializer(many=True, read_only=True, fields=("id", "name"), **{'validators': [], "required": False, 'allow_null': True})
    #company = CompanySerializer(**{'validators': [], "required": False, 'allow_null': True})

    def __init__(self, instance=None, data=None, **kwargs):
        fields: tuple = kwargs.pop("fields", None)
        partial = kwargs.pop("partial", False)
        self.invite_user = kwargs.pop("invite_user", False)
        super(UserSerializer, self).__init__(instance=instance, data=data, partial=partial, **kwargs)
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            # Drop any fields that are not specified in the `fields` argument.
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def to_internal_value(self, data):
        """
        If groups or job_set are passed along in request.data they will most
        likely be a single int or str or a list[str or int]. These values need to be
        converted to [ {key : value} ] for the serializer to validate them.
        """
        # if isinstance(data, int) or isinstance(data, str):
        #     return super().to_internal_value({"id": data})
        # groups = data.get("groups", None)
        # job_set = data.get("job_set", None)
        # print("job_set", job_set)
        # if groups != None:
        #     if isinstance(groups, list):
        #         data["groups"] = [{"id": k for k in groups}]
        #     if isinstance(groups, int) or isinstance(groups, str):
        #         data["groups"] = [{"id": groups}]

        # if job_set != None:
        #     if isinstance(job_set, list):
        #         data["job_set"] = [{"id": k for k in job_set}]
        #     if isinstance(job_set, int) or isinstance(job_set, str):
        #         data["job_set"] = [{"id": job_set}]
        return super().to_internal_value(data)

    def run_validation(self, data):
        """
        By making f_user a read_only_field it will not be included
        in super.run_validation(data). Let the other fields be validated then
        use self.validate_f_user() to validate the f_user field and add it 
        to the validate_data to be returned to self.create().

        The reason for this is so I can use the request.user object instead of 
        request.user.id which causes the user to have to be fetched from the db again.

        Now that groups and job_set are set as read_only their data will not be validated so 
        that is done after everything else is validated.
        """
        validated_data = super().run_validation(data=data)
        
        groups = data.get("groups", None)
        job_set = data.get("job_set", None)
        validated_data["groups"] = self.validate_groups(groups)
        validated_data["job_set"] = self.validate_job_set(job_set)

        company = data.get("company", None)
        if company is not None:
            validated_data["company"] = self.validate_company(company)
        return validated_data

    def validate_company(self, company: Union[Company, str, int]) -> Company:
        """
        """
        errors = OrderedDict()
        if isinstance(company, int) or isinstance(company, str):
            try:
                company = Company.objects.get(pk=company)
            except Company.DoesNotExist:
                errors['company'] = f"Company with pk {company} does not exist."
                raise ValidationError(errors)
        return company

    def validate_job_set(self, job_set: Union[list[str], list[int], int, str, None]) -> Union[list[int], list[str]]:
        if job_set == None:
            return []
        elif isinstance(job_set, list):
            return job_set
        elif isinstance(job_set, int):
            return [job_set]
        elif isinstance(job_set, str):
            if job_set == '':
                return []
            else:
                return [job_set]
        else:
            raise ValidationError(("job_set must be one of the following Union[list[str], list[int], int, str, None]"))

    def validate_groups(self, groups: Union[list[str], list[int], int, str, None]) -> Union[list[int], list[str]]:
        if groups == None:
            return []
        elif isinstance(groups, list):
            return groups
        elif isinstance(groups, int):
            return [groups]
        elif isinstance(groups, str):
            if groups == '':
                return []
            else:
                return [groups]
        else:
            raise ValidationError(("groups must be one of the following Union[list[str], list[int], int, str, None]"))

    def create(self, validated_data):
        """
        1. groups and job_set are now list[int] or list[str].

        2. if the invite_user kwarg is set to true then an email is sent. If the 
        email is sent successfully create an InviteToken row. Else raise a validation error.
        """
        if self.invite_user:
            token = rand_password(settings.LOGIN_TOKEN_LENGTH)
                #if the email address is valid create the user and the invite token
            sent, error = EmailManager.send_email(
                    "You are invited.", 
                    "Hello", 
                    validated_data["email"], 
                    "invite_user.html", 
                    {"token" : token, "url" : settings.FRONTEND_URL + f"/pm/token-login/"}
                )
            
            if not sent:
                raise ValidationError((error))
            else:
                user = CustomUser.objects.create_user(**validated_data)
                #add user to all the chosen jobs
                User_Job.objects.add_user_to_multiple_jobs(user, validated_data.get("job_set", None), user_being_created=True)
                #create invite token instance
                InviteToken.objects.create_token(user, token) 
        return user
    class Meta:
        model = CustomUser
        fields = '__all__'
        #exclude = ['password', "user_permissions", "is_active", "is_staff", "is_superuser"]
        read_only_fields = ["company"]
        extra_kwargs = {
            #have to be set write_only to True so it doesnt show up on a get request
            'password': {'write_only': True},
            #have to be set read_only to false to show up in validated_data
            'id': {'validators': [], "required": False, "read_only": False},
        }

        
class RFISerializer(serializers.ModelSerializer):
    """
    By specifying _from_user_key and to_users_key with the UserSerializer class when the
    RFI fields _from_user_key and to_users_key are serialized instead of it being a user_id it 
    will be the users corresponding email address or whatever fields are specified in the UserSerializer.
    """

    f_user = UserSerializer(fields=("id", "email"))
    t_user = UserSerializer(many=True, fields=("id", "email"))

    def __init__(self, instance=None, data=None, **kwargs):

        fields = kwargs.pop("fields", None)
        partial = kwargs.pop("partial", False)
        super(RFISerializer, self).__init__(instance=instance, data=data, partial=partial, **kwargs)
        super().__init__(instance=instance, data=data, partial=partial, **kwargs)
        if fields is not None:

            allowed = set(fields)
            existing = set(self.fields)
            # Drop any fields that are not specified in the `fields` argument.
            for field_name in existing - allowed:

                self.fields.pop(field_name)

    class Meta:
        model = RFI
        #fields = ("id", RFI_FROM, RFI_TO, RFI_SUBJECT, RFI_HAS_UNREAD_RESPONSES, RFI_BODY, RFI_DATE, RFI_STATUS) #"__all__"
        fields = "__all__"
        


class RFICreateUpdateSerializer(serializers.ModelSerializer):
    """
    This allows for fields to specified dynamically. When instantiating the serializer
    specify the needed fields by ResponseSerializer(data=data, field=('field 1', 'field 2')) or by
    not specifying any fields the serializer will expect all of the fields.
    """
    t_user = UserSerializer(many=True, fields=["id",])

    def __init__(self, instance=None, data=None, **kwargs):
        fields = kwargs.pop("fields", None)
        partial = kwargs.pop("partial", False)

        super(RFICreateUpdateSerializer, self).__init__(instance=instance, data=data, partial=partial, **kwargs)
        if fields is not None:

            allowed = set(fields)
            existing = set(self.fields)
            # Drop any fields that are not specified in the `fields` argument.
            for field_name in existing - allowed:

                self.fields.pop(field_name)

    class Meta:
        model = RFI
        fields = "__all__"
        read_only_fields = ("f_user", "company")
        extra_kwargs = {
            'id': {'validators': [], "required": False, "read_only": False},
        }

    def gather_ids(self, _list) -> list[int]:
        """
        The field t_user, which is either an int or list[int], is passed
        to the UserSerializer. It then returns a list[OrderedDict(["id", 1])]
        because of the many=True flag. This method parses out those ids and
        @returns list[int]
        """
        _ids = set()
        for _dict in _list:
            for v in _dict.values():
                _ids.add(v)
        return _ids

    def to_internal_value(self, data):
        """
        t_user can be a list[int], int or str.
        Convert it to [{"id": int}]
        """
        t_user = data.get("t_user", None)
        if t_user is not None:
            if isinstance(t_user, int) or isinstance(t_user, str):
                data["t_user"] = [{"id": t_user}]
            if isinstance(t_user, list):
                data["t_user"] = [{"id": v for v in t_user}]
        return super().to_internal_value(data)

    def run_validation(self, data):
        """
        By making f_user a read_only_field it will not be included
        in super.run_validation(data). Let the other fields be validated then
        use self.validate_f_user() to validate the f_user field and add it 
        to the validate_data to be returned to self.create().

        The reason for this is so I can use the request.user object instead of 
        request.user.id which causes the user to have to be fetched from the db again.
        """
        validated_data = super().run_validation(data=data)
        f_user = data.get("f_user", None)
        company = data.get("company", None)
        if f_user is not None:
            validated_data["f_user"] = self.validate_f_user(data["f_user"])
        if company is not None:
            validated_data["company"] = self.validate_company(data["company"])
        return validated_data

    def validate_f_user(self, f_user: Union[CustomUser, str, int]) -> CustomUser:
        """
        """
        errors = OrderedDict()
        if isinstance(f_user, int) or isinstance(f_user, str):
            try:
                f_user = CustomUser.objects.get(pk=f_user)
            except CustomUser.DoesNotExist:
                errors['user'] = f"User with pk {f_user} does not exist."
                raise ValidationError(errors)
        # else:
        #     serializer = UserSerializer(instance=f_user, fields=("id", "email"))
        return f_user

    def validate_company(self, company: Union[Company, str, int]) -> Company:
        """
        """
        errors = OrderedDict()
        if isinstance(company, int) or isinstance(company, str):
            try:
                company = Company.objects.get(pk=company)
            except Company.DoesNotExist:
                errors['company'] = f"Company with pk {company} does not exist."
                raise ValidationError(errors)
        return company

    def create(self, validated_data):
        """
        When an RFI is created need to check whether user added to the RFI is added to the corresponding
        job. If they are not added to the job add them. 
        """
        data = validated_data.copy()
        print("rfi creation data: ", data)
        job = data["job_key"]
        to_user_ids = self.gather_ids(data.pop("t_user"))

        rfi = RFI.objects.create_rfi(**data)
        #add all the t_users to the rfi
        User_RFI.objects.bulk_create_userids_w_rfi(rfi, to_user_ids)

        #add all the t_users that are not on the job
        User_Job.objects.add_users_to_1_job(job, to_user_ids)
                
        return rfi

    def update(self, instance, validated_data):
        #have to update the last_updated to now
        #on each update
        validated_data["last_updated"] = timezone.make_aware(datetime.now())
        return super().update(instance, validated_data)
        

class ResponseSerializer(serializers.ModelSerializer):

    """
    This allows for fields to specified dynamically. When instantiating the serializer
    specify the needed fields by ResponseSerializer(data=data, field=('field 1', 'field 2')) or by
    not specifying any fields the serializer will expect all of the fields.
    """
    _from_user_key = UserSerializer(fields=("id", "email"))

    def __init__(self, instance=None, data=None, **kwargs):

        fields = kwargs.pop("fields", None)
        super(ResponseSerializer, self).__init__(instance=instance, data=data, **kwargs)
        if fields is not None:

            allowed = set(fields)
            existing = set(self.fields)
            # Drop any fields that are not specified in the `fields` argument.
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = MyResponse
        fields = "__all__"

class ResponseCreateUpdateSerializer(serializers.ModelSerializer):

    """
    This allows for fields to specified dynamically. When instantiating the serializer
    specify the needed fields by ResponseSerializer(data=data, field=('field 1', 'field 2')) or by
    not specifying any fields the serializer will expect all of the fields.
    """

    def __init__(self, instance=None, data=None, **kwargs):

        fields = kwargs.pop("fields", None)
        super(ResponseCreateUpdateSerializer, self).__init__(instance=instance, data=data, **kwargs)
        if fields is not None:

            allowed = set(fields)
            existing = set(self.fields)
            # Drop any fields that are not specified in the `fields` argument.
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def run_validation(self, data):
        """
        By making f_user a read_only_field it will not be included
        in super.run_validation(data). Let the other fields be validated then
        use self.validate_f_user() to validate the f_user field and add it 
        to the validate_data to be returned to self.create().

        The reason for this is so I can use the request.user object instead of 
        request.user.id which causes the user to have to be fetched from the db again.
        """
        validated_data = super().run_validation(data=data)
        f_user = data.get("f_user", None)
        if f_user is not None:
            validated_data["f_user"] = self.validate_f_user(data["f_user"])
        return validated_data

    def validate_f_user(self, f_user: Union[CustomUser, str, int]) -> CustomUser:
        """
        """
        errors = OrderedDict()
        if isinstance(f_user, int) or isinstance(f_user, str):
            try:
                f_user = CustomUser.objects.get(pk=f_user)
            except CustomUser.DoesNotExist:
                errors['user'] = "User with pk {} does not exist.".format(f_user)
                raise ValidationError(errors)
        # else:
        #     serializer = UserSerializer(instance=f_user, fields=("id", "email"))
        return f_user

    def create(self, validated_data):
        f_user = validated_data["f_user"]
        rfi: RFI = validated_data["rfi"]
        #get all of the t_users on the RFI. add f_user as well.
        all_user_emails = User_RFI.objects.find_users_on_rfi(rfi) + [f_user.email]
        #notify all users of the new Response.
        sent, error = EmailManager.send_email(
            rfi.subject, 
            "This RFI has a new response.",
            all_user_emails,
            "new_rfi_response.html",
            {}
            )
        return MyResponse.objects.create(**validated_data)

    class Meta:
        """
        By making f_user a read_only_field it will not be included
        in super.run_validation(data). Let the other fields be validated then
        use self.validate_f_user() to validate it and add it to the validate_data
        to be returned.

        The reason for this is so I can use the request.user object instead of 
        request.user.id which causes the user to have to be fetched from the db again.
        """
        model = MyResponse
        fields = "__all__"
        read_only_fields = ("f_user",)


class JobSerializer(serializers.ModelSerializer):
    
    assigned_users = UserSerializer(many=True, fields=("id", "email"))
    class Meta:
        model = Job
        fields = ("id", "name", "date_created", "assigned_users")