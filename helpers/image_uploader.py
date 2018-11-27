from google.cloud import storage
import os


def upload_image(img):
    gcs = storage.Client()
    bucket = gcs.get_bucket(os.environ.get("GCS_BUCKET"))
    blob = bucket.blob(img.filename)
    blob.upload_from_string(
        img.read(),
        content_type=img.content_type
    )
    return blob.public_url
