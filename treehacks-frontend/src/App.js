import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css';
import GradioEmbed from './GradioEmbed'; // Adjust the path based on your file structure

function App() {
  const [sentences, setSentences] = useState([]);
  const [randomSentence, setRandomSentence] = useState('');
  const [capturedImage, setCapturedImage] = useState(null);
  const [showStartButton, setShowStartButton] = useState(true);
  const [showDoneButton, setShowDoneButton] = useState(false);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

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

            setTimeout(() => captureImage(stream), 3000);
          }
        })
        .catch((err) => {
          console.error("Error accessing camera:", err);
        });
    }

    setShowStartButton(false);
    setShowDoneButton(true);
  };

  const captureImage = (stream) => {
    if (canvasRef.current && videoRef.current) {
      const context = canvasRef.current.getContext('2d');
      canvasRef.current.width = videoRef.current.videoWidth;
      canvasRef.current.height = videoRef.current.videoHeight;
      context.drawImage(videoRef.current, 0, 0, canvasRef.current.width, canvasRef.current.height);
      const imageUrl = canvasRef.current.toDataURL('image/png');
      setCapturedImage(imageUrl);

      // Stop camera stream
      stream.getTracks().forEach(track => track.stop());
      videoRef.current.srcObject = null;
    }
  };

  const handleDoneClick = () => {
    if (capturedImage) {
      const formData = new FormData();
      formData.append('image', dataURLtoFile(capturedImage, 'captured-image.png'));
  
      axios.post('/api/process_image', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      .then(response => {
        // 백엔드에서 처리한 결과 사용
        console.log(response.data.result);
      })
      .catch(error => {
        console.error('Error processing image:', error);
      });
    }
  
    setShowStartButton(true);
    setShowDoneButton(false);
  };
  
  // Data URL을 File 객체로 변환하는 함수
  function dataURLtoFile(dataurl, filename) {
    let arr = dataurl.split(','), mime = arr[0].match(/:(.*?);/)[1],
        bstr = atob(arr[1]), n = bstr.length, u8arr = new Uint8Array(n);
    while(n--){
        u8arr[n] = bstr.charCodeAt(n);
    }
    return new File([u8arr], filename, {type:mime});
  }
  

  return (
    <div className="App">
      <header className="App-header">
      <div style={{ position: 'absolute', top: '0', left: '0', padding: '20px', display: 'flex', alignItems: 'center' }}>
        <h5>Empathicare</h5>
        <img src="logo.png" alt="Logo"  style={{ paddingLeft: '10px', width: '20px', height: '20px'}}/>
      </div>
        <h3>Situation:</h3>
        <h3>"I've noticed significant improvement in my symptoms, thanks to your advice."</h3>
        {showStartButton && <button onClick={handleStartClick}>Start</button>}
        {showDoneButton && <button onClick={handleDoneClick}>Done</button>}
        <GradioEmbed />
        
        {/* <h2>{randomSentence}</h2> */}
        
        <h5>The health care professional did a good job remaining positive!</h5>
        {capturedImage && <img src={capturedImage} alt="Captured" style={{ width: '300px' }} />}
        <video ref={videoRef} style={{ display: 'none' }}></video>
        <canvas ref={canvasRef} style={{ display: 'none' }}></canvas>
      </header>
    </div>
  );
}

export default App;

