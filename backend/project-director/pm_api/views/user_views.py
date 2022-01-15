from django.contrib.auth.models import Group
from django.conf import settings
from django.contrib.auth import get_user_model
from django.apps import apps as django_apps
from django.shortcuts import get_object_or_404

from rest_framework.decorators import action
from rest_framework.fields import empty
from rest_framework import serializers, viewsets, status
from rest_framework.response import Response

from ..serializers import GroupSerializer, UserSerializer
from ..utils import track_queries, parse_params, rand_password
from ..models import User_Job
from ..constants import *


CustomUser = get_user_model()
InviteToken = django_apps.get_model(settings.TOKEN_AUTH_MODEL, require_ready=True)
EmailManager = settings.IMPORT_STRING(settings.EMAIL_MANAGER)

class UserViewSet(viewsets.ModelViewSet):
    serializer_classes = {
        "update": UserSerializer,
        "partial_update": UserSerializer
    }
    query_sets = {
        "update": CustomUser.objects.all,
        "partial_update": CustomUser.objects.all,
    }
    def create(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
    @track_queries
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(*[instance], **{"data": request.data, "partial": partial, "fields": [f for f in request.data.keys()]})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    #@track_queries
    def list(self, request, *args, **kwargs):
        """
        Only return users that are apart of request.user's company. Can use query 
        params to filter the queryset even more. Example http://127.0.0.1:8000/api/d1/pm/user/?pk=1
        """
        params, valid = parse_params(request, CustomUser)
        if not valid:
            return Response({
                    "error": 
                    f"{params} is not a valid query parameter for model {CustomUser.__name__}."
                    }, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        queryset = CustomUser.objects.filter(company=request.user.company, **params).prefetch_related(*("groups",))
        serializer = UserSerializer(queryset, data=empty, many=True, fields=("id", "email", "groups", "is_active", "is_staff"))
        return Response({"details": "Users were successfully retrieve.", "results": serializer.data}, status=status.HTTP_200_OK)

    #@track_queries
    def retrieve(self, request, pk=None):
        if pk == None:
            return Response({"error": "User id is required."}, status=status.HTTP_400_BAD_REQUEST)
        queryset = CustomUser.objects.filter(pk=pk).prefetch_related(*("groups", "job_set"))
        if not queryset.exists():
            return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(queryset, data=empty, many=True, fields=("id", "email", "first_name", "last_name", "groups", "job_set"))
        return Response({"details": "User was successfully retrieved.", "results": serializer.data}, status=status.HTTP_200_OK)

    #@track_queries
    @action(detail=False, methods=['get'])
    def who_am_i(self, request, *args, **kwargs):
        serializer = UserSerializer(instance=request.user, data=empty, fields=("id", "email", "company", "first_name", "last_name"))
        return Response({"details": "User was successfully retrieved.", "results": serializer.data}, status=status.HTTP_200_OK)
    
    #@track_queries
    @action(detail=False, methods=['post'])
    def invite_user(self, request, *args, **kwargs):
        """
        Invites the potentially new user via email. If the email address is not valid response with a 400.
        Else create the user, if a job_key is sent with the request add the user to all of those jobs, and then
        create an invite token that is sent to them via email.
        """
        #expected structure of request.data
        _data = {
           "first_name": request.data.get("first_name"),
           "last_name": request.data.get("last_name"),
           "company": request.user.company,
           "email": request.data.get("email"),
           "password": rand_password(), 
           "job_set": request.data.get('job_set'), #can be a list [1, 2, 3] or a single value 1  
           "groups": request.data.get("group_set") #can be a list [1, 2, 3] or a single value 1
       }
        serializer = UserSerializer(data=_data, invite_user=True, fields=(k for k in _data.keys()))
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"details": "User was created successfully.", "results": serializer.data}, status=status.HTTP_201_CREATED)

    def get_serializer(self, *args, **kwargs):
        return self.serializer_classes[self.action](*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        return self.query_sets[self.action](*args, **kwargs)

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        obj = get_object_or_404(self.get_queryset(), **{self.lookup_field: self.kwargs[lookup_url_kwarg]})
        return obj

class GroupsViewSet(viewsets.ModelViewSet):

    pagination_class = None

    def create(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def retrieve(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request, *args, **kwargs):

        #queryset = self.filter_queryset(self.get_queryset())
        params, valid = parse_params(request, Group)
        if not valid:
            return Response({"error": f"{params} is not a valid query parameter."}, status=status.HTTP_400_BAD_REQUEST)
        queryset = Group.objects.all().filter(**params)
        serializer = GroupSerializer(queryset, many=True)
        return Response({"results": serializer.data}, status=status.HTTP_200_OK)

    def get_serializer(self, *args, **kwargs):
        return GroupSerializer()