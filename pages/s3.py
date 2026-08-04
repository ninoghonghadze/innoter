import logging
import uuid
import boto3
from django.conf import settings

logger = logging.getLogger(__name__)

def upload_image_to_s3(file_obj, original_filename):
    extension = original_filename.split(".")[-1]
    key = f"page-images/{uuid.uuid4()}.{extension}"

    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )
    s3.upload_fileobj(file_obj, settings.AWS_STORAGE_BUCKET_NAME, key)
    url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{key}"
    logger.info(f"Uploaded image to S3: {url}")
    return url
