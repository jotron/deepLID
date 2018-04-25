# using http://flask.pocoo.org/docs/0.12/
# help from https://gitlab.com/fast-science/background-removal-server/blob/master/webapp/app.py
# in order to record audio on IOS, https would be needed

# tools for webserver
import os
from flask import Flask, request, url_for, render_template

# tools for prediction
from keras.models import load_model
from numpy import expand_dims
import numpy as np
import librosa
import kapre
import tensorflow as tf

# retrieve trained model
model = load_model('../models/test.h5', custom_objects={'Melspectrogram':kapre.time_frequency.Melspectrogram}) #compile=false
graph = tf.get_default_graph()

# path to temporarily store upload
UPLOAD_path = 'uploads/sample.wav'

# initialize
app = Flask(__name__)

# prediction
def predict(file_path):
    signal, sr = librosa.load(file_path, sr=16000)

    if (len(signal) < 5*16000):
        print("recording to short")
        print(len(signal))

    # add batch and channel dimension
    resized_signal = signal[None, None, :5*16000]
    with graph.as_default():
        prediction = model.predict(resized_signal)
    resized_prediction = prediction[0]
    return resized_prediction.tolist()

# Website
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file_path = os.path.join(os.path.dirname(__file__), UPLOAD_path)
            file.save(file_path)
            pred = predict(file_path)
            #print(pred)
            return render_template('prediction.html', french_prob=str(pred[0]),
                                                      english_prob=str(pred[1]),
                                                      german_prob=str(pred[2]))
    else:
        return render_template('site.html', name="cool")


# serve public, https
if __name__ == "__main__":
    app.run(host='0.0.0.0', ssl_context=('cert.pem', 'key.pem'),
            port=5042, debug=True)
