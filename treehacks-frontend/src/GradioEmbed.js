import React from 'react';

const GradioEmbed = () => {
  return (
    <div style={{ width: '100%' }}>
      <iframe
        src="http://localhost:7860/" // Replace this URL with the actual URL of your Gradio app
        width="100%"
        height="400px"
        title="Gradio Interface"
      ></iframe>
    </div>
  );
};

export default GradioEmbed;
