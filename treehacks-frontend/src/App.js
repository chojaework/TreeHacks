import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css';
import GradioEmbed from './GradioEmbed'; // Adjust the path based on your file structure

function App() {
  const [sentences, setSentences] = useState([]);
  const [randomSentence, setRandomSentence] = useState('');
  const [showStartButton, setShowStartButton] = useState(true);
  const [showResultButton, setShowResultButton] = useState(false);
  const [showCancelButton, setShowCancelButton] = useState(false);
  const [recordedChunks, setRecordedChunks] = useState([]);
  const videoRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const recordedVideoRef = useRef(null);

  useEffect(() => {
    axios.get('/script.txt')
      .then(response => {
        const sentencesArray = response.data.split('\n');
        setSentences(sentencesArray);
      })
      .catch(error => {
        console.error('Error fetching sentences:', error);
      });
  }, []);

  const handleStartClick = () => {
    if (sentences.length > 0) {
      const randomIndex = Math.floor(Math.random() * sentences.length);
      setRandomSentence(sentences[randomIndex]);
    }

    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      const constraints = { video: true };

      navigator.mediaDevices.getUserMedia(constraints)
        .then((stream) => {
          if (videoRef.current) {
            videoRef.current.srcObject = stream;
            videoRef.current.play();

            // MediaRecorder setup
            const mediaRecorder = new MediaRecorder(stream);
            mediaRecorderRef.current = mediaRecorder;
            mediaRecorder.ondataavailable = (event) => {
              if (event.data.size > 0) {
                setRecordedChunks((prev) => [...prev, event.data]);
              }
            };
            mediaRecorder.start();
          }
        })
        .catch((err) => {
          console.error("Error accessing camera:", err);
        });
    }

    setShowStartButton(false);
  };

  const handleDoneClick = () => {
    // 녹화 중지
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
    }
  
    // 카메라 스트림 중지
    if (videoRef.current && videoRef.current.srcObject) {
      videoRef.current.srcObject.getTracks().forEach(track => track.stop());
      videoRef.current.srcObject = null;
    }
  
    // 상태 업데이트
    setShowResultButton(true); // 결과 버튼 표시
    setShowStartButton(true); // 시작 버튼 다시 표시
    setShowCancelButton(false); // 취소 버튼 숨김
  };
  
  

  const handleCancelClick = () => {
    setRandomSentence('');

    if (videoRef.current && videoRef.current.srcObject) {
      videoRef.current.srcObject.getTracks().forEach(track => track.stop());
      videoRef.current.srcObject = null;
    }

    setShowStartButton(true);
    setShowResultButton(false);
    setRecordedChunks([]);
  };

  const handleResultClick = () => {
    if (recordedChunks.length) {
      const blob = new Blob(recordedChunks, { type: 'video/webm' });
      const url = URL.createObjectURL(blob);
      if (recordedVideoRef.current) {
        recordedVideoRef.current.src = url;
        recordedVideoRef.current.play();
      }
    }
  };

  

  return (
    <div className="App">
      <header className="App-header">
        <img src="logo.png" alt="Logo" className="App-logo" style={{ paddingTop: '20px', width: '120px', height: '120px'}}/>
        <h1>Team Name</h1>
        <GradioEmbed />
        {showStartButton && <button onClick={handleStartClick}>Start</button>}
        {!showStartButton && <button onClick={handleDoneClick}>Done</button>}
        <h2>{randomSentence}</h2>
        <button onClick={handleCancelClick}>Cancel</button>
        {showResultButton && <button onClick={handleResultClick}>Result</button>}
        {!showStartButton && !showResultButton && <p>You are being recorded</p>}
        {showResultButton && <video ref={recordedVideoRef} style={{ width: '300px' }} controls></video>}
      </header>
    </div>
  );
  
}

export default App;

