from flask import Flask, render_template, redirect, url_for, request
#import google.cloud
app = Flask(__name__)
app.config['SECRET_KEY'] = 'I have a dream'
@app.route('/image', methods=['GET', 'POST'])

def detect_text(path):
    path = request.args.get('url')
    """Detects text in the file."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')

    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))
    return texts
