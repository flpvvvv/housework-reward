from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
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


@api_view(["POST"])
def add_housework_record(request):
    data = request.data.copy()
    
    if "image" in request.FILES:
        image = request.FILES["image"]
        file_extension = image.name.split(".")[-1]
        filename = f"{uuid.uuid4()}.{file_extension}"

        client = get_minio_client()

        if not client.bucket_exists(settings.MINIO_BUCKET_NAME):
            client.make_bucket(settings.MINIO_BUCKET_NAME)

        # Get the file size
        file_size = image.size

        client.put_object(
            settings.MINIO_BUCKET_NAME,
            filename,
            image,
            length=file_size,  # Use the actual file size
            content_type=image.content_type,
        )
        
        # Generate URL and add it to the data
        url = client.presigned_get_object(settings.MINIO_BUCKET_NAME, filename)
        data["image"] = url
    
    serializer = HouseworkRecordSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def add_contributor(request):
    serializer = ContributorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
def update_contributor(request, pk):
    try:
        contributor = Contributor.objects.get(pk=pk)
    except Contributor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ContributorSerializer(contributor, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_contributor(request, pk):
    try:
        contributor = Contributor.objects.get(pk=pk)
    except Contributor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    contributor.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["PUT"])
def update_housework_record(request, pk):
    try:
        record = HouseworkRecord.objects.get(pk=pk)
    except HouseworkRecord.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = request.data.copy()

    # Ensure we keep the existing contributor if not provided
    if "contributor_name" not in data:
        data["contributor_name"] = record.contributor.name

    if "image" in request.FILES:
        image = request.FILES["image"]
        file_extension = image.name.split(".")[-1]
        filename = f"{uuid.uuid4()}.{file_extension}"

        client = get_minio_client()

        if not client.bucket_exists(settings.MINIO_BUCKET_NAME):
            client.make_bucket(settings.MINIO_BUCKET_NAME)

        image_data = image.read()
        client.put_object(
            settings.MINIO_BUCKET_NAME,
            filename,
            image.file,
            length=len(image_data),
            content_type=image.content_type,
        )

        url = client.generate_presigned_url("GET", settings.MINIO_BUCKET_NAME, filename)
        data["image"] = url
    elif "image" not in data:
        # Keep existing image if not provided in request
        data["image"] = record.image

    serializer = HouseworkRecordSerializer(record, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_housework_record(request, pk):
    try:
        record = HouseworkRecord.objects.get(pk=pk)
    except HouseworkRecord.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    record.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def list_housework_records(request):
    records = HouseworkRecord.objects.all().order_by("-record_time")
    paginator = StandardResultsSetPagination()
    paginated_records = paginator.paginate_queryset(records, request)
    serializer = HouseworkRecordSerializer(paginated_records, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(["GET"])
def list_contributors(request):
    contributors = Contributor.objects.all().order_by("name")
    paginator = StandardResultsSetPagination()
    paginated_contributors = paginator.paginate_queryset(contributors, request)
    serializer = ContributorSerializer(paginated_contributors, many=True)
    return paginator.get_paginated_response(serializer.data)
