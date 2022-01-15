from django.http.response import FileResponse
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404


from rest_framework.views import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.fields import empty
from rest_framework import viewsets
from rest_framework.decorators import action, parser_classes

import json

from ..serializers import RFISerializer, RFICreateUpdateSerializer
from ..utils import parse_params, track_queries
from ..models import Attachment, RFI
from ..constants import *

CustomUser = get_user_model()


class RfiViewSet(viewsets.ModelViewSet):

    """
    1. when using self.get_serializer() use this syntax:
        A. serializer = self.get_serializer()(instance=instance, data=data)
    2. if this isnt done on the dynamic serializers it wont initialize correctly
    """
    serializer_classes = {
        "retrieve": RFISerializer,
        "list": RFISerializer,
        "create": RFICreateUpdateSerializer,
        "update": RFICreateUpdateSerializer,
        "partial_update": RFICreateUpdateSerializer,
    }

    querysets = {
        "list": RFI.objects.filter_rfis_by_user_permission,
    }

    additional_query_params = {
        "date_created"
    }

    def destroy(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, pk=None):
        rfi = get_object_or_404(RFI, pk=pk)
        serializer = self.get_serializer()(instance=rfi, data=empty)
        return Response({"results": serializer.data}, status=status.HTTP_200_OK)

    @track_queries
    def list(self, request):
        """
        Returns, if need be, a paginated list of rfis based on the 
        given query parameters.
        """
        params, valid = parse_params(request, RFI)
        if not valid:
            return Response({
                    "error": 
                    f"{params} is not a valid query parameter for model {RFI.__name__}."
                    }, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        queryset = self.get_queryset()(request.user, params)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer()
        if page is not None:
            serializer = serializer(page, many=True, fields=RFI_LIST_FIELDS)
            return self.get_paginated_response(serializer.data)
        serializer = serializer(queryset, many=True, fields=RFI_LIST_FIELDS)
        return Response({"results": serializer.data}, status=status.HTTP_200_OK)

    @track_queries
    @parser_classes((MultiPartParser, FormParser))
    def create(self, request, *args, **kwargs):
        #print("create RFI request data: ", request.data)
        _data = {
            "f_user": request.user.id,
            "job_key": request.data["job_key"],
            "company": request.user.company.id,
            #"t_user": [int(_pk['id']) for _pk in json.loads(request.data['t_user'])],
            "t_user": request.data['t_user'],#can be list[int], int, or str
            "subject": request.data["subject"],
            "body": request.data["body"],
            #attachments: files #attachment can be included in the request too.
        }
        serializer = self.get_serializer()(data=_data, fields=[f for f in _data.keys()]+["id"])
        serializer.is_valid(raise_exception=True)
        #attachment_ids = self.perform_create(request, serializer)
        self.perform_create(request, serializer)
        #return Response({"details": "rfi was successfully created.", "results": serializer.data, "attachments": attachment_ids}, status=status.HTTP_201_CREATED)
        return Response({"details": "RFI was successfully created.", "results": serializer.data}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        Same as the rest_framework except the fields that are updated are dynamically set by
        the request.
        """
        partial = kwargs.pop('partial', False)
        instance = get_object_or_404(RFI, pk=self.kwargs["pk"])
        serializer = self.get_serializer()(instance, data=request.data, partial=partial, fields=[k for k in request.data.keys()]) 
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response({"detail" : "rfi was updated successfully", "results" : serializer.data}, status=status.HTTP_200_OK)

    def perform_create(self, request, serializer):
        """
        Bulk creates the attachments in request.data.getlist("attachments)
        """
        rfi_instance = serializer.save()
        Attachment.objects.bulk_create([Attachment(upload=f, filename=f.name, rfi=rfi_instance) for f in request.data.getlist('attachments')])
        #return [a.id for a in attachments]

    # def filter_queryset(self, queryset):
    #     return super().filter_queryset(queryset)

    def get_serializer(self, *args, **kwargs):
        return self.serializer_classes[self.action]

    def get_queryset(self):
        return self.querysets[self.action]


class AttachmentViewSet(viewsets.ModelViewSet):
    """ 
    """
    querysets = {
        "preview": Attachment.objects.filter
    }

    def list(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

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


    @track_queries
    @action(detail=True, methods=["get"])
    def preview(self, request, pk=None, *args, **kwargs):
        """
        Only returns the id and filename. The attachments are not downloaded.
        
        pk: is an rfi primary key

        url format: /attachment/pk/preview/
        """
        print("...................requesting attachments..............")
        results = [{"id": a["id"], "filename": a["filename"]} for a in self.get_queryset()(rfi_id=pk).values()]
        print("attachment results: ", results, pk)
        return Response({"results": results}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def download(self, request, pk=None, *args, **kwargs):
        """
        Downloads the file and sends it to the frontend.

        pk: is an attachment primary key

        url format: /attachment/pk/download/
        """
        instance = get_object_or_404(Attachment, pk=pk)
        #response = FileResponse(instance.upload, as_attachment=True, filename=instance.filename)
        #response['Content-Disposition'] = 'attachment; filename="%s"' % instance.upload
        #response['Content-Disposition'] = 'attachment; filename="%s"' % instance.filename

        #as_attachment=True makes the browser ask the user if they want to download this
        return FileResponse(instance.upload, as_attachment=True, filename=instance.filename)

    def get_queryset(self):
        return self.querysets[self.action]
