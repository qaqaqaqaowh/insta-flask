from google.cloud import storage
import os
import io
import json


def upload_image(img):
    gcs = None
    if os.environ.get("FLASK_ENV"):
        gcs = storage.Client()
    else:
        from google.oauth2 import service_account
        gcs = storage.Client(credetials=service_account.Credentials.from_service_account_info(
            json.load(io.StringIO('{"asd": 123}'))))
    bucket = gcs.get_bucket(os.environ.get("GCS_BUCKET"))
    blob = bucket.blob(img.filename)
    blob.upload_from_string(
        img.read(),
        content_type=img.content_type
    )
    return blob.public_url