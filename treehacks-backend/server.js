const express = require('express');
const { PythonShell } = require('python-shell');
const multer = require('multer');
const fs = require('fs');
const path = require('path');

const app = express();
const upload = multer({ dest: 'uploads/' });

app.post('/api/process_image', upload.single('image'), (req, res) => {
  if (!req.file) {
    return res.status(400).send('No image uploaded.');
  }

  const options = {
    mode: 'text',
    pythonPath: 'python', // Python 설치 경로에 따라 변경 가능
    scriptPath: './', // Python 스크립트 위치
    args: [req.file.path] // Python 스크립트로 전달할 인자
  };

  PythonShell.run('process_image.py', options, (err, results) => {
    if (err) {
      console.error(err);
      res.status(500).send('Error processing image.');
    } else {
      // Python 스크립트의 출력 결과 사용
      res.send({ result: results[0] });
    }

    // 임시 이미지 파일 삭제
    fs.unlinkSync(req.file.path);
  });
});

const port = 5000;
app.listen(port, () => console.log(`Server running on port ${port}`));
