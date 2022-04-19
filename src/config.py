import os

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

IBM_S3_ENDPOINT = "https://s3.eu-de.cloud-object-storage.appdomain.cloud"
IBM_BUCKET_NAME = "libi"

FORECAST_WINDOW = 7 * 24
