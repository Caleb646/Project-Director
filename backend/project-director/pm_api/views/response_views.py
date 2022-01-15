from django.http.response import JsonResponse
from django.conf import settings

from rest_framework.views import Response
from rest_framework.decorators import parser_classes
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework import status, viewsets
from rest_framework.parsers import FormParser, MultiPartParser

import json

from ..serializers import ResponseSerializer, ResponseCreateUpdateSerializer
from ..utils import parse_params, track_queries
from ..constants import *
from ..models import Response as MyResponse, Attachment

EmailManager = (settings.EMAIL_MANAGER)


class ResponseViewSet(viewsets.ModelViewSet):

    serializer_classes = {
        "list": ResponseSerializer,
        "create": ResponseCreateUpdateSerializer
    }

    querysets = {
        "list": MyResponse.objects.filter
    }

    def list(self, request, *args, **kwargs):
        """
        Serializes all of the response associated with a particular rfi

        @required query params: rfi
        """
        params, valid = parse_params(request, MyResponse, required_params={"rfi"})
        if not valid:
            return Response({
                    "error": 
                    f"{params} is either not a valid query parameter or it was required and not included for model {MyResponse.__name__}."
                    }, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        serializer = self.get_serializer()(
                self.get_queryset()(**params), 
                many=True, 
                fields=[f.name for f in MyResponse._meta.get_fields()]
            )
        return Response({"results": serializer.data}, status=status.HTTP_200_OK)

    @track_queries
    @parser_classes((MultiPartParser, FormParser))
    def create(self, request, *args, **kwargs):
        data = {
            "f_user": request.user,
            "rfi": request.data["rfi"],
            "subject": request.data["subject"],
            "body": request.data["body"],
        }
        serializer = self.get_serializer()(data=data, fields=[k for k in data.keys()])
        serializer.is_valid(raise_exception=True)
        #attachment_ids = self.perform_create(serializer, request)
        self.perform_create(serializer, request)
        #print("\n\n", f"serializer data: {serializer.data}", "\n\n")
        #return JsonResponse({"detail": "response was successfully created.", "results": serializer.data, "attachments": attachment_ids}, status=status.HTTP_201_CREATED)
        return Response({"detail": "response was successfully created.", "results": serializer.data}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer, request):
        """
        Create any attachments sent with the response.
        """
        response = serializer.save()
        Attachment.objects.bulk_create([Attachment(upload=f, filename=f.name, rfi=response.rfi) for f in request.data.getlist('attachments')])
        #return [a.id for a in attachments]

    def retrieve(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get_queryset(self):
        return self.querysets[self.action]

    def get_serializer(self, *args, **kwargs):
        return self.serializer_classes[self.action]

