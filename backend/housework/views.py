from rest_framework import viewsets
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .serializers import HouseworkRecordSerializer, ContributorSerializer
from minio import Minio
from django.conf import settings
import uuid
from .models import Contributor, HouseworkRecord
from PIL import Image
import io


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

    def process_image(self, image_file):
        img = Image.open(image_file)
        
        # Convert RGBA to RGB if necessary
        if img.mode in ('RGBA', 'LA'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1])
            img = background
        
        # Calculate new dimensions while maintaining aspect ratio
        max_size = 2048
        ratio = min(max_size/img.width, max_size/img.height)
        if ratio < 1:
            new_size = (int(img.width * ratio), int(img.height * ratio))
            img = img.resize(new_size, Image.LANCZOS)
        
        # Save to bytes buffer
        buffer = io.BytesIO()
        format = image_file.content_type.split('/')[-1].upper()
        if format == 'JPEG':
            img.save(buffer, format=format, quality=80)
        else:
            img.save(buffer, format=format)
        buffer.seek(0)
        return buffer, format.lower()

    def handle_image_upload(self, image):
        processed_image, format = self.process_image(image)
        filename = f"{uuid.uuid4()}.{format}"
        client = get_minio_client()
        client.put_object(
            settings.MINIO_BUCKET_NAME,
            filename,
            processed_image,
            length=processed_image.getbuffer().nbytes,
            content_type=f"image/{format}"
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
