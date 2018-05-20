// Links to Useful Tutorials & Api's
//   https://github.com/muaz-khan/RecordRTC
//   https://github.com/muaz-khan/WebRTC-Experiment/issues/48
//   http://air.ghost.io/recording-to-an-audio-file-using-html5-and-js/
(function() {

    // get elements from webpage
    var recorder = document.getElementById("recorder"); // start record
    var uploader = document.getElementById("uploader"); // upload record
    var progress_bar = document.getElementById("progress"); // progress bar

    //disable upload button as long as no recording present
    uploader.disabled = true;

    //ajax form to POST
    formData = new FormData();

    //When start button is clicked
    recorder.onclick = function() {

        //record only audio
        var mediaConstraints = { video: false, audio: true };

        //make sure upload-button is disabled (in case of mutliple recordings)
        uploader.disabled = true;

        //access device
        navigator.mediaDevices.getUserMedia(mediaConstraints)
        .then(function(stream) {

            var recordRTC = RecordRTC(stream, { recorderType: StereoAudioRecorder,
                                                mimeType: 'audio/wav',
                                                numberOfAudioChannels: 1,
                                                desiredSampleRate: 16000,
                                                onAudioProcessStarted: progress_move()});
            // set duration of recording 5s
            recordRTC.setRecordingDuration(5 * 1000)
            .onRecordingStopped(function(url) {
                    blob = recordRTC.getBlob();
                    formData.append('file', blob);
                    uploader.disabled = false;

                    // insert recording after progress bar
                    var audio_element = '<audio src="' + url + '" controls></audio>';
                    progress_bar.parentElement.insertAdjacentHTML('afterend', audio_element);
            })

            // start recording request
            recordRTC.startRecording();
        })
        .catch(function(error) {console.log(error)});
    }

    //When upload button is clicked
    uploader.onclick = function() {

        // New post request to /
        var xhr = new XMLHttpRequest();
        xhr.open('POST', "/", true);
        xhr.send(formData);

        // display response as innerHTML of "pred_container"
        xhr.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                document.getElementById("pred_container").innerHTML = this.responseText;
            }
        };
    }

    //Animate progress bar
    function progress_move() {
        var width = 0; // start: 0%
        var id = setInterval(frame, 10); // every 10ms add 1/5% => total 5s
        function frame() {
            if (width >= 100) {
                clearInterval(id);
            } else {
                width += 1/5;
                progress_bar.style.width = width + '%';
            }
        }
}

})();
