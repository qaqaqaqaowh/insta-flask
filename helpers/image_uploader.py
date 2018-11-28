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
        cred = service_account.Credentials.from_service_account_info(
            json.load(io.StringIO(os.environ.get(
                "GOOGLE_APPLICATION_CREDENTIALS"))))
        gcs = storage.Client(project=cred.project_id, credentials=cred)
    bucket = gcs.get_bucket(os.environ.get("GCS_BUCKET"))
    blob = bucket.blob(img.filename)
    blob.upload_from_string(
        img.read(),
        content_type=img.content_type
    )
    return blob.public_url
