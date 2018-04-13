# using http://flask.pocoo.org/docs/0.12/
import os
from flask import Flask, request, url_for, render_template

UPLOAD_path = 'uploads/sample.wav'

app = Flask(__name__)
"""
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            print(os.path.join(os.path.dirname(__file__), UPLOAD_path))
            file.save(os.path.join(os.path.dirname(__file__), UPLOAD_path))

    return render_template('site.html', name="cool")
"""
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            print(os.path.join(os.path.dirname(__file__), UPLOAD_path))
            file.save(os.path.join(os.path.dirname(__file__), UPLOAD_path))

    return render_template('site.html', name="cool")
