from flask import Flask, request
from flask import Flask, render_template, redirect, url_for, request
from google.cloud import datastore
from google.cloud import storage
from google.cloud import vision


import os
import logging
from datetime import datetime
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
            image_file.read(), content_type=image_file.content_type)

    # Make the blob publicly viewable.
    blob.make_public()
     # Create a Cloud Vision client.
    vision_client = vision.ImageAnnotatorClient()

    # Use the Cloud Vision client to detect a face for our image.
    source_uri = 'gs://{}/{}'.format(CLOUD_STORAGE_BUCKET, blob.name)
    image = vision.types.Image(
        source=vision.types.ImageSource(gcs_image_uri=source_uri))
    document = vision_client.text_detection(image).full_text_annotation
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
    entity['text'] = document

    # Save the new entity to Datastore.
    datastore_client.put(entity)
    def draw_boxes(image, bounds, color,width=5):
        draw = ImageDraw.Draw(image)
        for bound in bounds:
            draw.line([
            bound.vertices[0].x, bound.vertices[0].y,
            bound.vertices[1].x, bound.vertices[1].y,
            bound.vertices[2].x, bound.vertices[2].y,
            bound.vertices[3].x, bound.vertices[3].y,
            bound.vertices[0].x, bound.vertices[0].y],fill=color, width=width)
        return image
    def get_document_bounds(response, feature):
        for i,page in enumerate(document.pages):
            for block in page.blocks:
                if feature==FeatureType.BLOCK:
                    bounds.append(block.bounding_box)
                for paragraph in block.paragraphs:
                    if feature==FeatureType.PARA:
                        bounds.append(paragraph.bounding_box)
                    for word in paragraph.words:
                        for symbol in word.symbols:
                            if (feature == FeatureType.SYMBOL):
                                bounds.append(symbol.bounding_box)
                        if (feature == FeatureType.WORD):
                            bounds.append(word.bounding_box)
        return bounds
    bounds=get_document_bounds(response, FeatureType.WORD)
    image= draw_boxes(image,bounds, 'yellow')
    def assemble_word(word):
        assembled_word=""
        for symbol in word.symbols:
            assembled_word+=symbol.text
        return assembled_word
    def find_word_location(document,word_to_find):
        for page in document.pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        assembled_word=assemble_word(word)
                        if(assembled_word==word_to_find):
                            return word.bounding_box

    location=find_word_location(document,'TRACKING')
    def text_within(document,x1,y1,x2,y2):
        text=""
        for page in document.pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        for symbol in word.symbols:
                            min_x=min(symbol.bounding_box.vertices[0].x,symbol.bounding_box.vertices[1].x,symbol.bounding_box.vertices[2].x,symbol.bounding_box.vertices[3].x)
                            max_x=max(symbol.bounding_box.vertices[0].x,symbol.bounding_box.vertices[1].x,symbol.bounding_box.vertices[2].x,symbol.bounding_box.vertices[3].x)
                            min_y=min(symbol.bounding_box.vertices[0].y,symbol.bounding_box.vertices[1].y,symbol.bounding_box.vertices[2].y,symbol.bounding_box.vertices[3].y)
                            max_y=max(symbol.bounding_box.vertices[0].y,symbol.bounding_box.vertices[1].y,symbol.bounding_box.vertices[2].y,symbol.bounding_box.vertices[3].y)
                            if(min_x >= x1 and max_x <= x2 and min_y >= y1 and max_y <= y2):
                                text+=symbol.text
                                if(symbol.property.detected_break.type==1 or
                                symbol.property.detected_break.type==3):
                                    text+=' '
                                if(symbol.property.detected_break.type==2):
                                    text+='\t'
                                if(symbol.property.detected_break.type==5):
                                    text+='\n'
        return text

    tracking_id =text_within(document, location.vertices[1].x, location.vertices[1].y, 30+location.vertices[1].x+(location.vertices[1].x-location.vertices[0].x),location.vertices[2].y)

    return tracking_id
