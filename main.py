from flask import Flask, request
from flask import Flask, render_template, redirect, url_for, request
from google.cloud import datastore
from google.cloud import storage
from google.cloud import vision


import os
import time
CLOUD_STORAGE_BUCKET = os.environ.get('CLOUD_STORAGE_BUCKET')
app = Flask(__name__)

@app.route('/scan', methods=['POST'])
def open_file():

    image_file = request.files['file']
     # Create a Cloud Storage client.
    storage_client = storage.Client()

    # Get the bucket that the file will be uploaded to.
    bucket = storage_client.get_bucket(CLOUD_STORAGE_BUCKET)
     # Create a new blob and upload the file's content.
    blob = bucket.blob(image_file.filename)
    blob.upload_from_string(
            photo.read(), content_type=image_file.content_type)

    # Make the blob publicly viewable.
    blob.make_public()
     # Create a Cloud Vision client.
    vision_client = vision.ImageAnnotatorClient()

    # Use the Cloud Vision client to detect a face for our image.
    source_uri = 'gs://{}/{}'.format(CLOUD_STORAGE_BUCKET, blob.name)
    image = vision.types.Image(
        source=vision.types.ImageSource(gcs_image_uri=source_uri))
    labels = vision_client.text_detection(image).full_text_annotations
    # Create a Cloud Datastore client.
    datastore_client = datastore.Client()

    # Fetch the current date / time.
    current_datetime = datetime.now()

    # The kind for the new entity.
    kind = 'labels'

    # The name/ID for the new entity.
    name = blob.name

    # Create the Cloud Datastore key for the new entity.
    key = datastore_client.key(kind, name)
     # Construct the new entity using the key. Set dictionary values for entity
    # keys blob_name, storage_public_url, timestamp, and text.
    entity = datastore.Entity(key)
    entity['blob_name'] = blob.name
    entity['image_public_url'] = blob.public_url
    entity['timestamp'] = current_datetime
    entity['text'] = labels

    # Save the new entity to Datastore.
    datastore_client.put(entity)
    return labels
