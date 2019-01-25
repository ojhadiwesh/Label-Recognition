from flask import Flask, request, render_template, jsonify
from pytesseract import image_to_string
UPLOAD_FOLDER = '/static'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/label', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
         if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files('file')
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template('signup.html')
