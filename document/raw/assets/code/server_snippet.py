@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        request_file = request.files['file']
        if request_file:
            # Virtuelle Datei generieren
            tmp_file = io.BytesIO(request_file.stream.read())
            # Abfrage an Modell
            pred = predict(tmp_file)
            # HTML als Antowrt senden
            return render_template('prediction.html',
                                   french_prob=str(pred[0]),
                                   english_prob=str(pred[1]),
                                   german_prob=str(pred[2]))
    else:
        # Web-Interface Standard Seite verschicken
        return render_template('site.html')
