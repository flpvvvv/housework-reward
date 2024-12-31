from minio import Minio
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def ensure_minio_bucket():
    """Ensure MinIO bucket exists, create if it doesn't"""
    try:
        client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE
        )

        # Check if bucket exists
        if not client.bucket_exists(settings.MINIO_BUCKET_NAME):
            # Create bucket with default options
            client.make_bucket(settings.MINIO_BUCKET_NAME)
            logger.info(f"Created MinIO bucket: {settings.MINIO_BUCKET_NAME}")
        else:
            logger.info(f"MinIO bucket already exists: {settings.MINIO_BUCKET_NAME}")

    except Exception as e:
        logger.error(f"Failed to ensure MinIO bucket exists: {str(e)}")
        raise
