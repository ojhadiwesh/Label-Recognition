from flask import Flask, request, render_template, jsonify


app = Flask(__name__)
@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        return jsonify(request.form['userID'], request.form['file'])
    return render_template('signup.html')
app.run(port= 5002, debug=True)
