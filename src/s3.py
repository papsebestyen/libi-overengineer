import io

import boto3

from .config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    IBM_BUCKET_NAME,
    IBM_S3_ENDPOINT,
)


class FileStorage:
    def __init__(
        self,
        endpoint: str = IBM_S3_ENDPOINT,
        access_key: str = AWS_ACCESS_KEY_ID,
        private_access_key: str = AWS_SECRET_ACCESS_KEY,
        bucket_name: str = IBM_BUCKET_NAME,
    ) -> None:
        self.s3_resource = boto3.resource(
            "s3",
            endpoint_url=endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=private_access_key,
        )
        self.bucket = self.s3_resource.Bucket(bucket_name)

    def upload_bytes(self, file_bytes: bytes, file_name: str) -> None:
        self.bucket.put_object(Body=file_bytes, Key=file_name)

    def download_bytes(self, file_name: str) -> io.BytesIO:
        s3_response_object = self.bucket.Object(key=file_name).get()
        object_content = s3_response_object["Body"].read()
        return io.BytesIO(object_content)
