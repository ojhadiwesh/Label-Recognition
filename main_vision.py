from flask import Flask, request
from google.cloud import vision
from flask import Flask, render_template, redirect, url_for, request
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'I have a dream'

app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/static'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB


class UploadForm(FlaskForm):
    photo = FileField(validators=[FileAllowed(photos, u'Image Only!'), FileRequired(u'Choose a file!')])
    submit = SubmitField(u'Upload')
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
@app.route('/scan', methods=['GET', 'POST'])
def open_file(filename):
    file_url = photos.url(filename)
    #path = requests.get(file_url)
    client = vision.ImageAnnotatorClient()

    with io.open(file_url, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    #print('Texts:')

    return render_template('browser.html', file_url=file_url, file_text=texts)


app. run(port =8080)
