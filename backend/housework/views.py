from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import HouseworkRecordSerializer
from minio import Minio
from django.conf import settings
import uuid

# Create your views here.

@api_view(['POST'])
def add_housework_record(request):
    serializer = HouseworkRecordSerializer(data=request.data)
    
    if serializer.is_valid():
        if 'image' in request.FILES:
            image = request.FILES['image']
            # Generate unique filename
            file_extension = image.name.split('.')[-1]
            filename = f"{uuid.uuid4()}.{file_extension}"
            
            # Upload to MinIO
            client = Minio(
                settings.MINIO_ENDPOINT,
                access_key=settings.MINIO_ACCESS_KEY,
                secret_key=settings.MINIO_SECRET_KEY,
                secure=settings.MINIO_SECURE
            )
            
            # Ensure bucket exists
            if not client.bucket_exists(settings.MINIO_BUCKET_NAME):
                client.make_bucket(settings.MINIO_BUCKET_NAME)
            
            # Upload file
            client.put_object(
                settings.MINIO_BUCKET_NAME,
                filename,
                image,
                image.size,
                image.content_type
            )
            
            # Update image field with MinIO path
            serializer.validated_data['image'] = f"minio://{settings.MINIO_BUCKET_NAME}/{filename}"
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
