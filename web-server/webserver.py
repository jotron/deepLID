# using http://flask.pocoo.org/docs/0.12/
# help from https://gitlab.com/fast-science/background-removal-server/blob/master/webapp/app.py

# tools for webserver
from flask import Flask, request, render_template

# tools for prediction
import io
from keras.models import load_model
import soundfile as sf
import kapre
import tensorflow as tf

# retrieve trained model
model = load_model('models/test.h5', custom_objects={'Melspectrogram':kapre.time_frequency.Melspectrogram}) #compile=false
graph = tf.get_default_graph()


# initialize
app = Flask(__name__)


# prediction
def predict(tmp_file):
    signal, samplerate = sf.read(tmp_file, dtype='float64')

    if (len(signal) < 5*16000):
        print("recording to short")
        print(len(signal))

    # add batch and channel dimension
    resized_signal = signal[None, None, :5*16000]
    with graph.as_default():
        prediction = model.predict(resized_signal)[0]
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
            # return html as response
            return render_template('prediction.html', french_prob=str(pred[0]),
                                                      english_prob=str(pred[1]),
                                                      german_prob=str(pred[2]))
    else:
        return render_template('site.html')


# serve public, https
if __name__ == "__main__":
    app.run(host='0.0.0.0',
            port=8181, debug=True)
