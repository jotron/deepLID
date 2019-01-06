# using http://flask.pocoo.org/docs/0.12/
# help from https://gitlab.com/fast-science/background-removal-server/blob/master/webapp/app.py

# tools for webserver
from flask import Flask, request, render_template

# tools for prediction
import io
from keras.models import load_model
import soundfile as sf
import librosa
import kapre
import tensorflow as tf
import numpy as np

# retrieve trained model
model = load_model('models/berlin_net/berlin_net.h5', custom_objects={'Melspectrogram':kapre.time_frequency.Melspectrogram}) #compile=false
graph = tf.get_default_graph()


# initialize
app = Flask(__name__)

# prediction
def predict(tmp_file):
    signal, sr = sf.read(tmp_file, dtype='float64')

    # not 16k sampleRate (safari)
    if (sr != 16000):
        signal = librosa.resample(signal, sr, 16000)
        sr = 16000

    # recording is too short (failing frontend)
    if (len(signal) < 5*16000):
        print("recording to short")
        print(len(signal))

    # add batch and channel dimension
    resized_signal = signal[None, None, :5*16000]
    with graph.as_default():
        prediction = model.predict(resized_signal)[0]

    # reformat
    prediction *= 100
    prediction = np.round(prediction, decimals=2)
    return prediction.tolist()


# Website
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        request_file = request.files['file']
        if request_file:
            # create virtual file
            tmp_file = io.BytesIO(request_file.stream.read())
            # ask prediction
            pred = predict(tmp_file)
            # sort predictions
            langs = ["French", "English", "German"]
            s_pred = sorted(zip(pred, langs), reverse=True)
            # return parsed XML
            return render_template('prediction.html', l1=str(s_pred[0][1]), p1=str(s_pred[0][0]),
                                                      l2=str(s_pred[1][1]), p2=str(s_pred[1][0]),
                                                      l3=str(s_pred[2][1]), p3=str(s_pred[2][0]),)
    else:
        # return homepage
        return render_template('site.html')


# serve public, https
if __name__ == "__main__":
    app.run(host='0.0.0.0',
            port=8181, debug=True)
