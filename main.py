from flask import Flask, request
from flask import Flask, render_template, redirect, url_for, request

import argparse
import base64
import httplib2

from apiclient.discovery import build
from oauth2client.client import GoogleCredentials

import os
import time

app = Flask(__name__)

@app.route('/scan', methods=['GET', 'POST'])
def open_file():
    image_file = request.files['file']
    API_DISCOVERY_FILE = 'https://vision.googleapis.com/$discovery/rest?version=v1'
    http = httplib2.Http()

    credentials = GoogleCredentials.get_application_default().create_scoped(
        ['https://www.googleapis.com/auth/cloud-platform'])
    credentials.authorize(http)

    service = build('vision', 'v1', http, discoveryServiceUrl=API_DISCOVERY_FILE)

    with open(image_file, 'rb') as image:
        image_content = base64.b64encode(image.read())
        service_request = service.images().annotate(
        body={
            'requests': [{
                'image': {
                'content': image_content
                },
                'features': [{
                    'type': 'TEXT_DETECTION'
                }]
            }]
        })
    response = service_request.execute()
    for results in response['responses']:
        if 'text_annotations' in results:
            for annotations in results['text_annotations']:
                return('Found label %s ' % (annotations['description']))
