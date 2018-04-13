// using https://github.com/muaz-khan/RecordRTC
// to post https://github.com/muaz-khan/WebRTC-Experiment/issues/48
// open issues: progress bar
(function() {

    var recorder = document.getElementById("recorder");
    var uploader = document.getElementById("uploader");

    //disable upload button as long as no recording present
    uploader.disabled = true;

    //ajax form to POST
    formData = new FormData();

    //Recording
    recorder.onclick = function() {
        var mediaConstraints = { video: false, audio: true };

        navigator.mediaDevices.getUserMedia(mediaConstraints)
        .then(function(stream) {
            var recordRTC = RecordRTC(stream, { type: 'audio' });

            recordRTC.setRecordingDuration(5 * 1000)
            .onRecordingStopped(function(url) {
                    //console.debug('setRecordingDuration', url);
                    //window.open(url);
                    blob = recordRTC.getBlob();
                    formData.append('file', blob);
                    uploader.disabled = false;
            })

            recordRTC.startRecording();
        })
        .catch(function(error) {console.log(error)});
    }

    //uploading
    uploader.onclick = function() {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', "/", true);
        xhr.send(formData);
    }

})();


/*function record(stream) {
    var recordRTC = RecordRTC(stream, { type: 'audio' });
    recordRTC.setRecordingDuration(5 * 1000).onRecordingStopped(function(url) {
            //console.debug('setRecordingDuration', url);
            window.open(url);
        })
    recordRTC.startRecording();
}
function activate() {
    var mediaConstraints = { video: false, audio: true };
    navigator.mediaDevices.getUserMedia(mediaConstraints).then(record).catch(function(error) {
        console.log("Error, perhaps an other application is using it");
    });
}*/
