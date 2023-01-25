import streamlit as st
import streamlit.components.v1 as components  # Import Streamlit

st.set_page_config(page_title='Mon Chaton - Care your cat', layout='wide')
# Layout
st.title(' 📸  Care On')
st.sidebar.markdown("#")

html = '''

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs/dist/tf.min.js" type="text/javascript"></script>
    <style>
        * {
          margin: 0;
          padding: 0;
        }
        html,
        body {
          width: 100%;
          height: 100%;
        }
        .wrapper {
          margin-top: 50px;
          height: 100%;
          overflow: hidden;
          display: flex;
          display-direction: column;
        }
        .video-container {
          display: flex;
          width: 900px;
          justify-content: pace-around;
        }
        .video-preview {
          margin-top: 210px;
          margin-left: 50px;
          display: flex;
          flex-direction: column;
        }
        .video-preview > video {
          width: 240px;
          height: 180px;
          border: 5px solid #DCB4A3;
          background-color : #DCB4A3;
        }
        .video-webcam > video {
          width: 520px;
          height: 390px;
          border: 5px solid #DCB4A3;
          background-color : #DCB4A3;
        }
        .button-container {
          display: flex;
          justify-content: flex-start;
        }
        .start-button{
          margin-right: auto;
        }
        p,
        .record-text{
          bottom: 0;
          font-size: 20px;
        }
        button,
        a {
          border: none;
          color: #fff;
          background: #ccc;
          padding: 0.5rem 1rem;
          cursor: pointer;
          font-size: 14px;
        }
        button:hover,
        a:hover {
          background: #F1D1C5;
        }
        button:focus {
          outline: none;
        }
        .active {
          background: #F1D1C5;
          /* background: #1565c0; */
        }
    </style>
</head>
  

  <body>
    <div class="wrapper">
      
      <div class="video-container">
        <div class="video-webcam">
          <div class="button-container">
            <button class="start-button">시작</button>
            <p id = 'record-img'> 녹화Off </p>
          </div>
          <video id="preview" autoplay muted></video>
        </div>
        
        <div class="video-preview">
          <div class="button-container">
            <a class="download-button">다운로드</a>
          </div>
          <video id="recording"></video>
        </div>
      </div>
    </div>
    

    <script src="https://www.gstatic.com/firebasejs/8.8.1/firebase-app.js"></script>
    <script src="https://www.gstatic.com/firebasejs/8.8.1/firebase-database.js"></script>
    <script src="https://www.gstatic.com/firebasejs/8.8.1/firebase-analytics.js"></script>
    <script src="https://www.gstatic.com/firebasejs/8.8.1/firebase-auth.js"></script>
    <script src="https://www.gstatic.com/firebasejs/8.8.1/firebase-firestore.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow-models/coco-ssd"></script>
    <script>
        // Buttons
        const startButton = document.querySelector(".start-button");
        const downloadButton = document.querySelector(".download-button");
        // Player
        const previewPlayer = document.querySelector("#preview");
        const recordingPlayer = document.querySelector("#recording");
        // setting
        const recordImg = document.getElementById('record-img');
        const recordingDuration = 10000;
        let recorder;
        let recordedChunks;
        var isRecord = false;
        
        var model = undefined;
        
        // functions
        function videoStart() {
          cocoSsd.load().then((loadedModel) => {
            model = loadedModel;
            console.log('loaded model!');
          });
          navigator.mediaDevices
            .getUserMedia({ video: true, audio: true })
            .then((stream) => {
              previewPlayer.srcObject = stream;
              previewPlayer.addEventListener('loadeddata', predictWebcam);  
              //recordButton.addEventListener("click", recordStart);
            });
        }
        
        const predictWebcam = () => {
          model.detect(previewPlayer).then((predictions) => {
            window.requestAnimationFrame(predictWebcam);
            for (let i = 0; i < predictions.length; i++) {
              if (predictions[i].class == 'cat'){
                if (isRecord == false){
                  isRecord=true;
                  recordStart();
                }   
              }  
            }
          });
        }
        
        function recordStart() {
            console.log('녹화시작: '+isRecord);
            recordImg.innerText = "녹화 On";
            startRecording(
              previewPlayer.captureStream() || previewPlayer.mozCaptureStream()
            );
            setTimeout("stopRecording()",recordingDuration)
        }
        
        function startRecording(stream) {
          recordedChunks = [];
          recorder = new MediaRecorder(stream);
          recorder.ondataavailable = (e) => recordedChunks.push(e.data);
          recorder.start();
        }
        
        function stopRecording() {
          //previewPlayer.srcObject.getTracks().forEach((track) => track.stop());
          isRecord=false;
          recordImg.innerText = "녹화 Off";
          console.log('녹화종료: ' + isRecord);
          recorder.stop();
          setTimeout("playRecording()", 1000)
        }
        
        function playRecording() {
          const recordedBlob = new Blob(recordedChunks, { type: "video/mp4" });
          recordingPlayer.src = URL.createObjectURL(recordedBlob);
          //recordingPlayer.play();
          downloadButton.href = recordingPlayer.src;
          downloadButton.download = `recording_1.mp4`;
          downloadButton.click();
        }
        
        // event
        startButton.addEventListener("click", videoStart);
        //stopButton.addEventListener("click", stopRecording);
        //playButton.addEventListener("click", playRecording);
        
        /* button ui */
        const buttons = document.querySelectorAll(".button-container > button");
        
        function setActive() {
          const activeButton = document.querySelector(".active");
          if (activeButton) {
            activeButton.classList.remove("active");
          }
          this.classList.add("active");
        }
        
        buttons.forEach((button) => button.addEventListener("click", setActive));

    </script>

  </body>


</html>

'''
components.html(html, width = 850, height = 500)
