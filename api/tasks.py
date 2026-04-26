from celery import shared_task
from api.models import Postcode
import csv
import io
import boto3
from django.conf import settings

PART_SIZE = 5 * 1024 * 10224
CHUNK_SIZE = 500

@shared_task(bind=True)
def create_csv(self, postcodes):
    filename = f"{self.request.id}.csv"

    minio = boto3.client(
        's3',
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )

    bucket = settings.AWS_STORAGE_BUCKET_NAME

    mpu = minio.create_multipart_upload(
        Bucket=bucket,
        Key=filename,
        ContentType='text/csv',
    )

    upload_id = mpu['UploadId']
    parts = []
    part_number = 1

    buffer = io.StringIO()
    writer = csv.writer(buffer)
    fields = [f.name for f in Postcode._meta.fields]
    writer.writerow(fields)

    result = Postcode.objects.filter(postcode__in=postcodes)


    try:
        for i, obj in enumerate(result.iterator(chunk_size=CHUNK_SIZE)):
            writer.writerow([getattr(obj, field) for field in fields])

            if buffer.tell() >= PART_SIZE:
                buffer.seek(0)
                part = minio.upload_part(
                    Bucket=bucket,
                    Key=filename,
                    PartNumber=part_number,
                    UploadId=upload_id,
                    Body=buffer.read().encode('utf-8'),
                )
                parts.append({'PartNumber': part_number, 'ETag': part['ETag']})
                part_number += 1
                buffer = io.StringIO()
                writer = csv.writer(buffer)

        if buffer.tell() > 0:
            buffer.seek(0)
            part = minio.upload_part(
                Bucket=bucket,
                Key=filename,
                PartNumber=part_number,
                UploadId=upload_id,
                Body=buffer.read().encode('utf-8'),
            )
            parts.append({'PartNumber': part_number, 'ETag': part['ETag']})

        minio.complete_multipart_upload(
            Bucket=bucket,
            Key=filename,
            UploadId=upload_id,
            MultipartUpload={'Parts': parts},
        )


    except Exception:
        minio.abort_multipart_upload(Bucket=bucket, Key=filename, UploadId=upload_id)
        raise

    return {'status': 'done', 'file': filename}