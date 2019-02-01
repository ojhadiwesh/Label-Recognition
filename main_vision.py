from flask import Flask, request
from google.cloud import vision
app = Flask(__name__)
app.config['SECRET_KEY'] = 'I have a dream'

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
