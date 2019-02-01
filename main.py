from flask import Flask, request

from flask import Flask, render_template, redirect, url_for, request

import os
import time

app = Flask(__name__)

@app.route('/scan/<filename>', methods=['GET', 'POST'])
def open_file(filename):
    image_url = requests.args.get('url')
    #path = requests.get(file_url)
    with open(image_url, 'rb') as image_file:
        content = base64.b64encode(image_file.read())
        content = content.decode('utf-8')

    api_key = "AIzaSyDn1BzcyAz1Yh0_H4thvEifVuVSjYO2_64"
    url = "https://vision.googleapis.com/v1/images:annotate?key=" + api_key
    headers = { 'Content-Type': 'application/json' }
    request_json = {
        'requests': [
            {
                'image': {
                    'content': content
                },
                'features': [
                    {
                        'type': "TEXT_DETECTION",
                        'maxResults': 10
                    }
                ]
            }
        ]
    }
    response = requests.post(
        url,
        json.dumps(request_json),
        headers
    )
    result = response.json()
    texts= (result['responses'][0]['textAnnotations'][0]['description'])

    return render_template('browser.html', file_url=file_url, file_text=texts)


app. run()
