from flask import Flask, request
from google.cloud import vision
from google.cloud.vision import types
from flask import Flask, render_template, redirect, url_for, request

import os
import time

app = Flask(__name__)

@app.route('/scan', methods=['GET', 'POST'])
def open_file(filename):
    file_url = request.args.get('url')
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = file_url
    resp = client.text_detection(image=image)
    print('\n'.join([d.description for d in resp.text_annotations]))

    return render_template('browser.html', file_url=file_url, file_text=resp.text_annotations)


app. run()
