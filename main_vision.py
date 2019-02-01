from flask import Flask, request
from google.cloud import vision
from flask import Flask, render_template, redirect, url_for, request
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
import os
import time

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        for filename in request.files.getlist('photo'):

            name = ('file' + str(time.time()))[:15]
            photos.save(filename, name=name + '.')
        success = True
    else:
        success = False
    return render_template('display.html', form=form, success=success)
@app.route('/scan/<filename>', methods=['GET', 'POST'])
def open_file(filename):
    image_url = requests.args.get('url')
    #path = requests.get(file_url)
    client = vision.ImageAnnotatorClient()

    with io.open(image_url, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    #print('Texts:')

    return render_template('browser.html', file_url=file_url, file_text=texts)


app. run(port =8080)
