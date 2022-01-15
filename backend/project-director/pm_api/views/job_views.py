

from rest_framework.fields import empty
from rest_framework import viewsets, status
from rest_framework.views import Response

from ..serializers import JobSerializer
from ..utils import parse_params, track_queries
from ..constants import *
from ..models import Job


class JobViewSet(viewsets.ModelViewSet):

    serializer_classes = {
        "list": JobSerializer
    }

    querysets = {
        "list": Job.objects.filter_by_user_permissions
    }

    def retrieve(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def create(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @track_queries
    def list(self, request, *args, **kwargs):
        params, valid = parse_params(request, Job)
        if not valid:
            return Response({
                    "error": 
                    f"{params} is not a valid query parameter for model {Job.__name__}."
                    }, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        queryset = self.get_queryset()(request.user, request.user.company, params)
        serializer = self.get_serializer()(queryset, data=empty, many=True)
        return Response({"details": "job were retrieved successfully", "results": serializer.data}, status=status.HTTP_200_OK)
    
    def get_serializer(self, *args, **kwargs):
        return self.serializer_classes[self.action]

    def get_queryset(self):
        return self.querysets[self.action]
        