from flask import Flask, request
from flask import Flask, render_template, redirect, url_for, request
from googleapiclient import discovery
from oauth2client import client
from oauth2client.contrib import appengine
from google.appengine.api import memcache
import argparse
import base64
import httplib2

from apiclient.discovery import build
from oauth2client.client import GoogleCredentials

import os
import time

app = Flask(__name__)

@app.route('/scan', methods=['GET', 'POST'])
def open_file(filename):
    API_DISCOVERY_FILE = 'https://vision.googleapis.com/$discovery/rest?version=v1'
    http = httplib2.Http()

    credentials = GoogleCredentials.get_application_default().create_scoped(
        ['https://www.googleapis.com/auth/cloud-platform'])
    credentials.authorize(http)

    service = build('vision', 'v1', http, discoveryServiceUrl=API_DISCOVERY_FILE)

    with open(photo_file, 'rb') as image:
        image_content = base64.b64encode(image.read())
        service_request = service.images().annotate(
        body={
            'requests': [{
                'image': {
                'content': image_content
                },
                'features': [{
                    'type': 'LABEL_DETECTION',
                    'maxResults': 5,
                }]
            }]
        })
    response = service_request.execute()
    for results in response['responses']:
        if 'labelAnnotations' in results:
            for annotations in results['labelAnnotations']:
                print('Found label %s, score = %s' % (annotations['description'],annotations['score']))
    return render_template('browser.html', file_url=file_url, file_text=results['labelAnnotations'])


app. run()
