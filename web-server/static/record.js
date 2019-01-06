// Links to Useful Tutorials & Api's
//   https://github.com/muaz-khan/RecordRTC
//   https://github.com/muaz-khan/WebRTC-Experiment/issues/48
//   http://air.ghost.io/recording-to-an-audio-file-using-html5-and-js/
//   https://github.com/muaz-khan/RecordRTC/blob/master/simple-demos/audio-recording.html
(function() {

    // get elements from webpage
    var recorder = document.getElementById("recorder"); // start record
    var uploader = document.getElementById("uploader"); // upload record
    var progress_bar = document.getElementById("bar"); // progress bar
    var audio_container = document.getElementById("audio_container");

    // count number of media recorders
    var num = 0;

    //disable upload button as long as no recording present
    uploader.disabled = true;

    // check if safari browser
    var isSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);

    //ajax form to POST
    formData = new FormData();

    //When start button is clicked
    recorder.onclick = function() {

        // increase num
        num = num + 1;

        //record only audio
        var mediaConstraints = { video: false, audio: true };

        //make sure upload-button and record-button are disabled
        recorder.disabled = true;
        uploader.disabled = true;

        //access device
        navigator.mediaDevices.getUserMedia(mediaConstraints)
        .then(function(stream) {

            // set options
            var options = { recorderType: StereoAudioRecorder,
                            mimeType: 'audio/wav',
                            numberOfAudioChannels: 1,
                            desiredSampleRate: 16000,
                            onAudioProcessStarted: progress_move()};

            if(isSafari) {
                options.sampleRate = 44100;
                options.bufferSize = 4096;
            }

            // init recordRTC
            var recordRTC = RecordRTC(stream, options);
            // set duration of recording 5s (6s to be sure)
            recordRTC.setRecordingDuration(6 * 1000)
            .onRecordingStopped(function(url) {

                    // insert recording data in Form
                    blob = recordRTC.getBlob();
                    formData.set('file', blob);

                    // show recording below progress bar
                    var audio_element = '<audio src="' + url + '" controls></audio>';
                    audio_container.innerHTML = audio_element;

                    // disconnect microphone
                    stream.stop();
                    stream = null;

                    // reenable buttons
                    uploader.disabled = false;
                    recorder.disabled = false;
            })

            // start recording request
            recordRTC.startRecording();
        })
        .catch(function(error) {
          // some browsers support only a limited amount of media objects
          if (num >= 2) {
            alert("Max number of recordings exceeded. Please Refresh.")
          }
          else {
            alert("Unable to capture your microphone.")
          }
          console.log(error)
        });
    }

    //When upload button is clicked
    uploader.onclick = function() {

        // New post request to '/'
        var xhr = new XMLHttpRequest();
        xhr.open('POST', "/", true);
        xhr.send(formData);

        // display response as innerHTML of "pred_container"
        xhr.onreadystatechange = function() {
            if (this.readyState == 4) { // process done
              if (this.status == 200) { // process success
                document.getElementById("pred_container").innerHTML = this.responseText;
              }
              else { // unsuccessful = server error
                alert(String(this.status) +": An error occurred")
              }
            }
        };
    }

    //Animate progress bar
    function progress_move() {
        var value = 0; // start: 0%
        var id = setInterval(frame, 120); // every 120ms add 2% => total 5s
        function frame() {
            if (value >= 100) {
                clearInterval(id);
            } else {
                value += 2;
                progress_bar.setAttribute('value', value);
            }
        }
}

})();
