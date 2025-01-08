from rest_framework import viewsets
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .serializers import HouseworkRecordSerializer, ContributorSerializer
from minio import Minio
from django.conf import settings
import uuid
from .models import Contributor, HouseworkRecord


def get_minio_client():
    return Minio(
        settings.MINIO_ENDPOINT,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        secure=settings.MINIO_SECURE,
    )


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class HouseworkRecordViewSet(viewsets.ModelViewSet):
    queryset = HouseworkRecord.objects.all().order_by('-record_time')
    serializer_class = HouseworkRecordSerializer
    pagination_class = StandardResultsSetPagination

    def handle_image_upload(self, image):
        file_extension = image.name.split(".")[-1]
        filename = f"{uuid.uuid4()}.{file_extension}"
        client = get_minio_client()
        client.put_object(
            settings.MINIO_BUCKET_NAME,
            filename,
            image,
            length=image.size,
            content_type=image.content_type,
        )
        return f"{settings.MINIO_BUCKET_NAME}/{filename}"

    def create(self, request, *args, **kwargs):
        data = request.data.dict() if hasattr(request.data, 'dict') else request.data
        if "image" in request.FILES:
            data["image"] = self.handle_image_upload(request.FILES["image"])
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data.dict() if hasattr(request.data, 'dict') else request.data
        
        if "image" in request.FILES:
            data["image"] = self.handle_image_upload(request.FILES["image"])
        
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save()


class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects.all().order_by('name')
    serializer_class = ContributorSerializer
    pagination_class = StandardResultsSetPagination
