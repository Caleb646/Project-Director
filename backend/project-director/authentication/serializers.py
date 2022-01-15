from django.contrib.auth import get_user_model
from django.conf import settings
from django.apps import apps as django_apps
from django.core.exceptions import ValidationError

from rest_framework import serializers

CustomUser = get_user_model()
Company = django_apps.get_model(settings.COMPANY_MODEL, require_ready=True)

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("id", "name")

class UserSerializer(serializers.ModelSerializer):

    company = CompanySerializer()

    def __init__(self, instance=None, data=None, **kwargs):
        fields: tuple = kwargs.pop("fields", None)
        partial = kwargs.pop("partial", False)
        self.super_user = kwargs.pop("super_user", False)

        super(UserSerializer, self).__init__(instance=instance, data=data, partial=partial, **kwargs)
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            # Drop any fields that are not specified in the `fields` argument.
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def create(self, validated_data):
        """
        Parse company name from ordered dict. Create the company 
        and pass it to the user.

        If self.super_user is True make the user a super user.

        Automatically checks if the company exists.
        """
        company = [v for k, v in validated_data["company"].items()][0]
        print("validated data: ", company)
        validated_data["company"] = Company.objects.create_company(name=company)
        if self.super_user:
            return CustomUser.objects.create_superuser(**validated_data)
        return CustomUser.objects.create_user(**validated_data)

    class Meta:
        model = CustomUser
        fields = '__all__'
        #exclude = ['password', "user_permissions", "is_active", "is_staff", "is_superuser"]
        extra_kwargs = {
            #have to be set write_only to True so it doesnt show up on a get request
            'password': {'write_only': True},
        }